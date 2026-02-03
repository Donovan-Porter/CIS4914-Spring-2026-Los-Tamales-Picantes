from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, jsonify
from flaskwebgui import FlaskUI

#TODO: fix quiz
from quiztest import Quiz, Question

# TODO: valerie matching game
from minigames.matching import MemoryGame
import uuid


import os, sys

# Huggingface transformers stuff
os.environ["HF_HUB_OFFLINE"] = "1" 
os.environ['TRANSFORMERS_OFFLINE'] = '1'
from transformers import pipeline
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
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
    # TODO: Stream chat without refreshing page

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
