from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, jsonify
from flaskwebgui import FlaskUI

#TODO: fix quiz
from quiztest import Quiz, Question

import argostranslate.package # TODO: See if this import is necessary
import argostranslate.translate

# TODO: valerie matching game
import matching_game

import os, sys

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


if __name__ == "__main__" :

    FlaskUI(app=app, server="flask").run()
