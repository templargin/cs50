import os

from flask import Flask, render_template, request
from flask import jsonify
from models import *

# set up database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("LOCAL_DB")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights = flights)

@app.route("/book", methods=["POST"])
def book():
    # getting name for booking
    name = request.form.get("name")

    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message = "Invalid flight number")

    # make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message = "There is no such flight")

    # insert name into the flight
    flight.add_passenger(name)

    return render_template("success.html")


@app.route("/flights")
def flights():
    flights = Flight.query.all()
    return render_template("flights.html", flights = flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message = "There is not such flight")

    passengers = flight.passengers

    return render_template("flight.html", flight = flight, passengers = passengers)


@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    # Make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error": "Invalid flight ID"}), 422


    # Get passengers
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)

    # Conver to JSON
    return jsonify({
    "origin":flight.origin,
    "destination":flight.destination,
    "duration":flight.duration,
    "passengers":names
    })
