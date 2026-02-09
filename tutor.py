from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for
from flaskwebgui import FlaskUI

#TODO: fix quiz
from quiztest import Quiz, Question

import argostranslate.package # TODO: See if this import is necessary
import argostranslate.translate

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


# Huggingface transformers stuff
os.environ["HF_HUB_OFFLINE"] = "1" 
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from transformers import pipeline
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# TODO: Find source and fix 'headertoolarge' error caused by pipeline on pulls from branches not don-dev
pipe = pipeline("text-generation", model=os.path.join(base_path, "model"))

app = Flask(__name__, static_folder="/")

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

    if "GET" == request.method :
        return render_template("chat.html")
    elif "POST" == request.method :
        print(request.form["chat-input"])
        input = request.form["chat-input"]

        messages = [
            {"role": "user", "content": input},
        ]
        out = pipe(messages)

        output = out[0]['generated_text'][1]['content']
        return render_template("chat.html", chat_output = input + '\n\n' + output)

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

# TODO: changing to dialogue based format with focus on conjugation (fill-in-the-blank style)

@app.route('/choose_course')
def choose_course():
    courses = find_vocab_dirs()
    return render_template('choose_course.html', courses=courses)

@app.route('/choose_chapter')
def choose_chapter():
    course = request.args.get('course')
    if not course:
        return redirect(url_for('choose_course'))
    dirpath = os.path.join(base_path, 'static', 'learning-resources', course)
    files = []
    try:
        files = sorted([f for f in os.listdir(dirpath) if f.endswith('.json')])
    except Exception:
        files = []
    return render_template('choose_chapter.html', course=course, files=files)

@app.route('/choose_vocab_group', methods=['GET','POST'])
def choose_vocab_group():
    course = request.values.get('course')
    vocab_file = request.values.get('file')
    if not course or not vocab_file:
        return redirect(url_for('choose_course'))
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
        vocab_list = [v.get('es','') for v in vocab_group.get('vocabulary', [])]

        # STATIC word bank (all vocab in the group)
        session['vocab_bank'] = vocab_list

        session['course'] = course
        session['file'] = vocab_file
        session['group_index'] = group_index
        session['group_title'] = vocab_group.get('title-es','')

        # TODO: shuffle order
        order = list(range(len(vocab_list)))
        random.shuffle(order)

        vocab_shuffled = [vocab_list[i] for i in order]
        session['vocab_list'] = vocab_shuffled

        story = generate_story_with_model(pipe, vocab_shuffled, title=vocab_group.get('title-es'))
        if not story:
            return 'Story generation failed.'
        
        # DYNAMIC answer list (only words actually used, in order)
        answer_vocab = [part['word'] for part in story]

        session['answer_vocab'] = answer_vocab 
        session['story'] = story
        session['revealed'] = [False] * len(vocab_shuffled)
        session['current_index'] = 0

        return redirect(url_for('story'))


    return render_template('choose_vocab_group.html', course=course, vocab_file=vocab_file, groups=groups)

@app.route('/story', methods=['GET','POST'])
def story():
    vocab_bank = session.get('vocab_bank', [])  # Static list of all vocab words
    answer_vocab = session.get('answer_vocab', [])  # Dynamic list of words used in the story

    story = session.get('story')
    if not story:
        return redirect(url_for('choose_course'))

    current = session.get('current_index', 0)
    revealed = session.get('revealed', [False]*len(story))
    message = None

    if request.method == 'POST':
        guess = request.form.get('guess','').strip()
        if current >= len(story):
            return redirect(url_for('story'))

        expected_word = story[current]['word']
        guess_n = normalize_text(guess)
        expected_n = normalize_text(expected_word)

        if guess_n == expected_n:
            revealed[current] = True
            session['revealed'] = revealed
            session['current_index'] = current + 1

            if session['current_index'] >= len(story):
                # finished
                return render_template(
                    'story.html',
                    story=story,
                    revealed=revealed,
                    finished=True,
                    current_index=current,
                    message=None,
                    vocab_list=vocab_bank,
                    answer_vocab=answer_vocab
                )

            return redirect(url_for('story'))
        else:
            message = 'Try again!'


    return render_template(
        'story.html',
        story=story,
        revealed=revealed,
        current_index=current,
        message=message,
        finished=False,
        vocab_list=vocab_bank,
        answer_vocab=answer_vocab
    )

if __name__ == "__main__" :

    FlaskUI(app=app, server="flask").run()
