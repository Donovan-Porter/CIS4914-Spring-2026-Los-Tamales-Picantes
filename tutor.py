from flask import Flask, render_template, send_from_directory
from flaskwebgui import FlaskUI

import os


app = Flask(__name__, static_folder="/")

@app.route('/favicon.ico')
def favicon() :
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index() :
    test_text = "Lorem Ipsum Dolor Sit Amet..."
    return render_template("index.html", index_testing=test_text)

@app.route("/chatbot-input>", methods = ['GET', 'POST', 'DELETE'])
def chatbot_input() :
    return render_template("chat.html")



if __name__ == "__main__" :

    FlaskUI(app=app, server="flask").run()
