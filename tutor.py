from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, jsonify
from flaskwebgui import FlaskUI

#TODO: fix quiz
from quiztest import Quiz, Question

import argostranslate.package # TODO: See if this import is necessary
import argostranslate.translate
# TODO: valerie matching game
from minigames.matching import MemoryGame
import uuid


import os, sys, json, random
# from conjugation_story import normalize_text, strip_article, find_grammar_dirs, generate_conjugation_story
from conjugation_convo import generate_conjugation_exercise_from_list, find_grammar_dirs, normalize_text

#
# ____/\____
#      O __|
#    _____|
# _/
#

# Global variables
lang_flow = "row"
en_src = True
message_role = {"role": "system", "content": "You are an insightful, patient, and knowledgable, tutor for the Spanish language."}
messages = [message_role]


# Huggingface transformers stuff
os.environ["HF_HUB_OFFLINE"] = "1" 
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from transformers import pipeline
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# TODO: Find source and fix 'headertoolarge' error caused by pipeline on pulls from branches not don-dev
pipe = pipeline("text-generation", model=os.path.join(base_path, "model"))

app = Flask(__name__, static_folder="/")

# Toggles
timerOn = True

# TODO: fix quiz (tutorial video: https://www.youtube.com/watch?v=PdHYd8N30_4)
app.secret_key = "quiz-dev-key"
quiz = Quiz()
quiz.add_question(Question("What is my name?", ['Poop', 'Poop1', 'Poop2'], 0))
quiz.add_question(Question("What is my age?", ['1', '12', '14'], 2))

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
    # TODO: Save chat history
    # TODO: Add Markdown support.
    # TODO: Make output pretty

    global messages
    output = []
    
    if "GET" == request.method :
        for n in range(1, len(messages)) :
            output.append(messages[n]['content'])
            
        return render_template("chat.html", chat_output = output)
    elif "POST" == request.method :
        print(request.form["chat-input"])
        input = request.form["chat-input"]

        messages.append({"role": "user", "content": input})
        #messages = [{"role": "user", "content": input}]
        #out = pipe(messages)
        out = pipe(messages, max_new_tokens=150)
        messages.append(out[0]["generated_text"][-1])

        for n in range(1, len(messages)) :
            output.append(messages[n]['content'])
   # output = output + messages[n]['content'] + '\n\n'
   
        print(output)

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

@app.route('/choose_course_convo')
def choose_course_convo():
    courses = find_grammar_dirs()  # same function as before
    return render_template('choose_course_convo.html', courses=courses)

@app.route('/choose_chapter_convo')
def choose_chapter_convo():
    course = request.args.get('course')
    if not course:
        return redirect(url_for('choose_course_convo'))

    dirpath = os.path.join(base_path, 'static', 'learning-resources', course)
    files = []
    try:
        files = sorted([f for f in os.listdir(dirpath) if f.endswith('.json')])
    except Exception:
        files = []

    return render_template('choose_chapter_convo.html', course=course, files=files)

@app.route('/choose_group_convo', methods=['GET','POST'])
def choose_group_convo():
    course = request.values.get('course')
    vocab_file = request.values.get('file')

    if not course or not vocab_file:
        return redirect(url_for('choose_course_convo'))
    
    path = os.path.join(base_path, 'static', 'learning-resources', course, vocab_file)
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
    except Exception as e:
        return f'Error loading vocab file: {e}'

    groups = data.get('groups', [])

    if request.method == 'POST':
        group_index = int(request.form.get('group_index', 0))
        grammar_group = groups[group_index]

        # List of verbs/phrases
        grammar_list = [ex['derivative'].strip().rstrip('.!?') for ex in grammar_group.get('examples', [])]
        random.shuffle(grammar_list)

        # Generate random conjugation exercises
        exercises = generate_conjugation_exercise_from_list(pipe, grammar_list)

        # Save in session
        session['convo_conjugation'] = exercises
        session['revealed_convo'] = [False]*len(exercises)
        session['current_index_convo'] = 0
        session['vocab_list_convo'] = grammar_list
        session['answer_vocab_convo'] = [ex['answer'] for ex in exercises]

        return redirect(url_for('convo_conjugation'))

    return render_template('choose_group_convo.html', course=course, vocab_file=vocab_file, groups=groups)

@app.route('/convo_conjugation', methods=['GET','POST'])
def convo_conjugation():
    exercises = session.get('convo_conjugation', [])
    if not exercises:
        return redirect(url_for('choose_course_convo'))

    current = session.get('current_index_convo', 0)
    revealed = session.get('revealed_convo', [False]*len(exercises))
    vocab_list = session.get('vocab_list_convo', [])
    answer_vocab = session.get('answer_vocab_convo', [])
    message = None

    if request.method == 'POST':
        guess = request.form.get('guess','').strip()
        if current >= len(exercises):
            return redirect(url_for('convo_conjugation'))

        expected_word = exercises[current]['answer']
        if normalize_text(guess) == normalize_text(expected_word):
            revealed[current] = True
            session['revealed_convo'] = revealed
            session['current_index_convo'] = current + 1
            if current + 1 >= len(exercises):
                return render_template(
                    'convo_conjugation.html',
                    story=exercises,
                    revealed=revealed,
                    finished=True,
                    current_index=current,
                    message=None,
                    vocab_list=vocab_list,
                    answer_vocab=answer_vocab
                )
            return redirect(url_for('convo_conjugation'))
        else:
            message = 'Try again!'

    return render_template(
        'convo_conjugation.html',
        story=exercises,
        revealed=revealed,
        current_index=current,
        finished=False,
        message=message,
        vocab_list=vocab_list,
        answer_vocab=answer_vocab
    )


# TODO: valerie matching game
# store each unique matching game
games = {}

# get the correct html for the matching game
@app.route("/matching_page")
def matching_page():
    return render_template("matching.html")


# create a matching game
@app.route("/matching", methods=["POST"])
def create_matching_game():
    returned_size = request.json.get("size", 4)

    # create a memory game with the size we are looking for
    game = MemoryGame(size = returned_size)

    # get the game id
    game_id = str(uuid.uuid4())
    games[game_id] = game
    return {"game_id": game_id, "state": game.state()}


# handle a card click
@app.route("/matching/<game_id>/click", methods=["POST"])
def click_card(game_id):
    # get the game
    game = games.get(game_id)

    # get the position of the card
    row = request.json.get("row")
    col = request.json.get("col")

    result = game.click_card(row, col)
    return result


if __name__ == "__main__" :

    FlaskUI(app=app, server="flask").run()
