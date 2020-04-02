import requests
import socket
import urllib.parse

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods = ["POST"])
def convert():

    # Parsing URL
    url = "http://data.fixer.io/api/latest"

    url_parse = urllib.parse.urlsplit(url)

    # Making sure hostname is resolved
    try:
        socket.gethostbyname(url_parse.hostname)
    except socket.error:
        print("ERROR: API request unsuccessful")

    # Parameters for HTTP request
    access_key = "2e3ee8f5320fb9ca89d63387caf8fcdd"

    currency = request.form.get("currency")

    # Send a request
    res = requests.get(url, params={"access_key":access_key, "symbols":currency})

    # Making sure request is successful
    if res.status_code != 200:
        return jsonify({"success": False})

    # Getting JSON data
    data = res.json()

    # Check if data is OK
    if not data["success"]:
        return jsonify({"success": False})

    if currency not in data["rates"]:
        return jsonify({"success": False})

    # Return the data
    return jsonify({"success": True, "rate": data["rates"][currency]})


if __name__ == "__main__":
    app.run()
