import requests

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

votes = {"yes":0, "no":0, "hz":0}

@app.route("/")
def index():
    return render_template("index.html", votes = votes)

@socketio.on("submit vote")
def vote(input):
    selection = input["votemarker"]
    votes[selection] += 1
    emit("vote results",votes,broadcast = True)

if __name__ == "__main__":
    app.run()
