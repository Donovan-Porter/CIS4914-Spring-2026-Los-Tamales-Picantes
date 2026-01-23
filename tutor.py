from flask import Flask, render_template, send_from_directory, request
from flaskwebgui import FlaskUI

import os

from transformers import pipeline

# Huggingface transformers stuff
os.environ['TRANSFORMERS_OFFLINE'] = '1'
pipe = pipeline("text-generation", model=os.path.join(os.getcwd(), "model"))

app = Flask(__name__, static_folder="/")

@app.route('/favicon.ico')
def favicon() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index() :
    test_text = "Lorem Ipsum Dolor Sit Amet..."
    return render_template("index.html", index_testing=test_text)

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


if __name__ == "__main__" :

    FlaskUI(app=app, server="flask").run()
