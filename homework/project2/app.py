import os
import requests
import eventlet

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {}
channels["general"] = []

users = []
limit = 100;

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def vote():
    emit("load channels", channels)


@socketio.on("username submitted")
def userSubmitted(data):
    username = data["username"]
    databack = {}
    if username in users:
        databack["success"] = False
    else:
        databack["success"] = True
        databack["username"] = username
        users.append(username)

    emit("add username", databack)


@socketio.on("channel submitted")
def channelSubmitted(data):
    channel_name = data["channel_name"]
    user = data["user"]
    databack = {}
    if channel_name in channels:
        databack["success"] = False
        databack["user"] = user
    else:
        databack["success"] = True
        databack["channel_name"] = channel_name
        databack["user"] = user
        channels[channel_name] = []

    emit("update channels", databack, broadcast = True)



@socketio.on("channel selected")
def channelSelected(data):
    activeChannel = data["activeChannel"]
    messages = channels[activeChannel]
    emit("show channel", messages)


@socketio.on("message sent")
def channelSelected(data):
    channel = data["channel"]
    message = {"text": data["text"], "time":data["time"], "user":data["user"]}
    channels[channel].append(message)
    if (len(channels[channel])>limit):
        channels[channel].pop(0)

    databack = {"text": message["text"], "time":message["time"], "user":message["user"], "channel":channel}

    emit("add message", databack, broadcast = True)



if __name__ == "__main__":
    socketio.run(app)
