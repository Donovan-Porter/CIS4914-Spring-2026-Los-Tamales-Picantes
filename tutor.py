from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, jsonify, abort, flash
from flaskwebgui import FlaskUI

import sqlite3
from local_db import LocalDB

#TODO: fix quiz
from quiztest import Quiz, Question

import argostranslate.translate

# TODO: valerie matching game
import matching_game

import os, sys, json, random
from short_story import normalize_text, strip_article, find_vocab_dirs, generate_story_with_model

#
# ____/\____
#      O __|
#    _____|
# _/
#

# Global variables
lang_flow = "row"
en_src = True
message_role = {"role": "system", "content": "insightful; patient; knowledgable, hispanic; Spanish; casual;"}
messages = [message_role]


# Huggingface transformers stuff
os.environ["HF_HUB_OFFLINE"] = "1" 
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from transformers import pipeline
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
pipe = pipeline("text-generation", model=os.path.join(base_path, "model"))

# Chatbot output sanitation using regular expression
from re import sub, compile
# Match any whitespace after punctuation == r'(?<=[!?.])\s*'
# Match a potential line starting with '#' or '*' (markdown headers) == r'(?:\n[#*]+[^\n]*\n)?'
# Match a potential number with arbitrary digits or non-whitespace followed by a period, e.g. '1.', 'a.', '-.', or '99.' (markdown lists) == r'(?:(?:\d+|\S)\.)?'
# Match an arbirary string until end of input unless is has ending punctuations like exclamation, single or double quotation, question, period, or tick mark (markdown code block) == r'[^!?.`"\']*$'
trailing = compile(r'(?<=[!?.])\s*(?:\n[#*]+[^\n]*\n)?(?:(?:\d+|\S)\.)?[^!?.`"\']*$')
# TODO: Improve the regular expression

app = Flask(__name__, static_folder="/")

# LOCAL DB
localdb_handler = LocalDB()

# Toggles
timerOn = True

# TODO: fix quiz (tutorial video: https://www.youtube.com/watch?v=PdHYd8N30_4)
app.secret_key = "quiz-dev-key"
quiz = Quiz()
quiz.add_question(Question("What is my name?", ['Poop', 'Poop1', 'Poop2'], 0))
quiz.add_question(Question("What is my age?", ['1', '12', '14'], 2))

def reset_login_session():
    session["local_login"] = False
    session["username"] = ""
    session["points"] = ""

@app.route('/favicon.ico')
def favicon() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index() :
    test_text = "Lorem Ipsum Dolor Sit Amet..."
    return render_template("index.html", index_testing=test_text)


@app.route("/toggleTimer", methods=['GET', 'POST'])
def toggle_timer():
    global timerOn
    
    if request.method == 'POST':
        status = request.get_json().get("status")
        timerOn = status
        return jsonify({"Timer Toggle Status": timerOn})
        
    if request.method == 'GET':
        return jsonify({'status' : timerOn})
 
    return jsonify({"Error Timer Toggle": "Error: Could not process /toggleTimer"})

@app.route("/profile", methods=["POST", "GET"])
def load_profile():
    if session.get("local_login") is True:
        return render_template("profile.html", username=session['username'], points=f"Points: {session['points']}")

    return redirect(url_for('sign_up'))

@app.route("/profile/logout", methods=["POST", "GET"])
def logout():
    reset_login_session()
    return redirect(url_for('login'))

@app.route("/profile/delete", methods=["POST", "GET"])
def delete():
    try:
        print("session", session["username"])
        res = localdb_handler.delete_user(session["username"])
        
        if res == 404:
            flash("ERROR 404: User not found.")
            return redirect(url_for('load_profile'))

    except Exception as e:
        print("Error occurred during profile deletion:", e)
        flash("An error has occurred.")

    finally:
        reset_login_session()
        return redirect(url_for('sign_up'))

@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form["username"]

        try:
            res = localdb_handler.create_user(username)
            
            if res == 409:
                flash("User already exists.")
                return redirect(url_for('login'))
            
            session["local_login"] = True
            session["username"] = localdb_handler.get_user(username)
            session["points"] = localdb_handler.get_points(username)
            return redirect(url_for('load_profile'))

        except Exception as e:
            print("Error occurred during sign up:", e)
            flash("An error occurred.")
            return redirect(url_for('sign_up'))

    reset_login_session()
    return render_template("sign-up.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        try:
            user = localdb_handler.get_user(username)
            
            if user is None:
                flash("Invalid user.")
                return redirect(url_for('login'))
            
            session["local_login"] = True
            session["username"] = user
            session["points"] = localdb_handler.get_points(username)

        except Exception as e:
            print("Error occurred during local sign up:", e)
            return redirect(url_for('login'))

        finally:
            return redirect(url_for('load_profile'))

    reset_login_session()
    return render_template("login.html")
    
@app.route("/start_quiz")
def start_quiz():
    session.clear()
    session['current_question'] = 0
    session['score'] = 0
    return redirect(url_for('quiz_view'))
    
@app.route("/quiz_view", methods=['GET', 'POST'])
def quiz_view():   
    if request.method == 'POST':
        selected_option = request.form.get('option')
        current_question_index = session.get('current_question')
        if selected_option is not None:
            correct_option = quiz.questions[current_question_index].correct_option
            if int(selected_option) == correct_option:
                session['score'] += 1
        
        session['current_question'] += 1
        if session['current_question'] >= len(quiz.questions):
            current_question_index = 0
            return redirect(url_for('results'))


    current_question_index = session.get('current_question')
    question = quiz.questions[current_question_index]
    return render_template('quiz.html', question=question, question_index=current_question_index + 1, total_questions = len(quiz.questions))

@app.route("/results")
def results():
    score = session.get('score')
    total_questions = len(quiz.questions)
    
    if score is None:
        score = 0
        
    return f'<h1>Your Score: {score}/{total_questions}</h1> <a href="/">Home</a>'        


@app.route("/chat", methods = ['GET', 'POST', 'DELETE'])
def chat() :
    # TODO: Add Markdown support.
    # TODO: Ensure ends in punctuation

    # Declared at top of file
    global messages
    output = []
    
    # First page load
    if "GET" == request.method :

        # Pre-loaded messages (see messages declaration)
        for n in range(1, len(messages)) :
            output.append(messages[n]['content'])
        # Render page with pre-loaded messages
        return render_template("chat.html", chat_output = output)
    # Update the logs
    elif "POST" == request.method :

        # Get form data submitted by page
        input = request.form["chat-input"]

        # Add data to 'messages' variable
        messages.append({"role": "user", "content": input})

        # Generate output
        out = pipe(messages, max_new_tokens=333)

        # Get generated string
        generated_string = out[0]["generated_text"][-1]

        # Strip any un-punctuated trailing bits
        # TODO: Test lag time of regular expression use; look into faster options
        global trailing
        new_content = generated_string["content"]

        generated_string["content"] = sub(trailing, "", new_content)
        new_content = generated_string["content"]

        # Add output to 'messages'
        # The LLM input is these chat logs
        messages.append(generated_string)

        # 'output' is local variable
        # Copy over messages so that chat history shows on the page
        # TODO: See if persistent variable is faster
        for n in range(1, len(messages)) :
            output.append(messages[n]['content'])

        return render_template("chat.html", chat_output = output)
    
@app.route("/chat/clear", methods = ['POST'])
def chat_clear():
    
    global messages, message_role
    
    if "POST" == request.method:
        messages.clear()
        messages = [message_role]
            
    return render_template("chat.html")

@app.route("/translate", methods = ['GET', 'POST'])
def translate() :
    global en_src
    global lang_flow

    if "GET" == request.method :
        return render_template("translate.html")

    elif "POST" == request.method :
        but_val = request.form.get("input_button")

        if "submit_input" == but_val :
            input = request.form["input"]
            if en_src :
                output = argostranslate.translate.translate(input, "en", "es")
            else :
                output = argostranslate.translate.translate(input, "es", "en")
            return render_template("translate.html", output = output, lang_flow=lang_flow)

        elif "switch_lang" == but_val :
            if en_src :
                en_src = False
                lang_flow = "row-reverse"
            else :
                en_src = True
                lang_flow = "row"

            return render_template("translate.html", lang_flow=lang_flow)

@app.route('/choose_course_vocabulary')
def choose_course_vocabulary():
    courses = find_vocab_dirs()
    return render_template('choose_course_vocabulary.html', courses=courses)

@app.route('/choose_chapter_vocabulary')
def choose_chapter_vocabulary():
    course = request.args.get('course')
    if not course:
        return redirect(url_for('choose_course_vocabulary'))
    dirpath = os.path.join(base_path, 'static', 'learning-resources', course)
    files = []
    try:
        files = sorted([f for f in os.listdir(dirpath) if f.endswith('.json')])
    except Exception:
        files = []
    return render_template('choose_chapter_vocabulary.html', course=course, files=files)

@app.route('/choose_group_vocabulary', methods=['GET','POST'])
def choose_group_vocabulary():
    course = request.values.get('course')
    vocab_file = request.values.get('file')
    if not course or not vocab_file:
        return redirect(url_for('choose_course_vocabulary'))
    path = os.path.join(base_path, 'static', 'learning-resources', course, vocab_file)
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except Exception as e:
        return f'Error loading vocab file: {e}'

    groups = data.get('groups', [])
    if request.method == 'POST':
        group_index = int(request.form.get('group_index', 0))

        vocab_group = groups[group_index]

        raw_vocab = [v.get('es','') for v in vocab_group.get('vocabulary', [])]

        session['vocab_bank'] = raw_vocab

        order = list(range(len(raw_vocab)))
        random.shuffle(order)

        vocab_shuffled = [raw_vocab[i] for i in order]
        session['vocab_list'] = vocab_shuffled
    
        story = generate_story_with_model(pipe, vocab_shuffled, title=vocab_group.get('title-es'))
        if not story:
            return 'Story generation failed.'
        
        # DYNAMIC answer list (only words actually used, in order)
        answer_vocab = [part['word'] for part in story]

        session['answer_vocab_vocabulary'] = answer_vocab 
        session['story_vocabulary'] = story
        session['revealed_vocabulary'] = [False] * len(vocab_shuffled)
        session['current_index_vocabulary'] = 0

        return redirect(url_for('story_vocabulary'))


    return render_template('choose_group_vocabulary.html', course=course, vocab_file=vocab_file, groups=groups)

@app.route('/story_vocabulary', methods=['GET','POST'])
def story_vocabulary():
    vocab_bank = session.get('vocab_bank', [])  # Static list of all vocab words
    answer_vocab = session.get('answer_vocab_vocabulary', [])  # Dynamic list of words used in the story

    story = session.get('story_vocabulary')
    if not story:
        return redirect(url_for('choose_course_vocabulary'))

    current = session.get('current_index_vocabulary', 0)
    revealed = session.get('revealed_vocabulary', [False]*len(story))
    message = None

    if request.method == 'POST':
        guess = request.form.get('guess','').strip()
        if current >= len(story):
            return redirect(url_for('story_vocabulary'))

        expected_word = story[current]['word']
        guess_n = normalize_text(guess)
        expected_n = normalize_text(expected_word)

        if guess_n == expected_n:
            revealed[current] = True
            session['revealed_vocabulary'] = revealed
            session['current_index_vocabulary'] = current + 1

            if session['current_index_vocabulary'] >= len(story):
                # finished
                return render_template(
                    'story_vocab.html',
                    story=story,
                    revealed=revealed,
                    finished=True,
                    current_index=current,
                    message=None,
                    vocab_list=vocab_bank,
                    answer_vocab=answer_vocab
                )

            return redirect(url_for('story_vocabulary'))
        else:
            message = 'Try again!'


    return render_template(
        'story_vocab.html',
        story=story,
        revealed=revealed,
        current_index=current,
        message=message,
        finished=False,
        vocab_list=vocab_bank,
        answer_vocab=answer_vocab
    )


# TODO: valerie matching game
@app.route("/matching_page")
def matching_page():
    '''
    get the correct html for the matching game
    '''
    return render_template("matching.html")

@app.route("/matching", methods=["POST"])
def create_matching_game():
    '''
    create a matching game
    '''
    returned_size = request.json.get("size", 4)
    spn_lvl = request.json.get("spanish_level", "spn1130")
    chp_num = request.json.get("chapter_number", 1)
    file_type = request.json.get("file_type", "Vocabulary")

    return matching_game.create_game(returned_size, spn_lvl, chp_num, file_type)

@app.route("/matching/<game_id>/click", methods=["POST"])
def click_card(game_id):
    '''
    handle a card click
    '''
    # get the position of the card
    row = request.json.get("row")
    col = request.json.get("col")
    return matching_game.handle_click_card(game_id, row, col)

# TODO: Remove the giant 'CAUSE ERROR' button in index, and remove this (or, keep it. Whatever.)
# Just for showing the `abort()` functionality
@app.route("/ERROR", methods=["GET"])
def ERROR() :
    abort(500)

@app.errorhandler(500)
def internal_error(error) :
    return render_template("500.html")

@app.errorhandler(409)
def conflict_error(error) :
    #flash("Input cannot be used.")
    pass


if __name__ == "__main__" :

    FlaskUI(app=app, server="flask").run()
