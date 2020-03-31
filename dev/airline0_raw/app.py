import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("LOCAL_DB"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    flights = db.execute("select * from flights").fetchall()
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
    if db.execute("select * from flights where id = :id", {"id":flight_id}).rowcount == 0:
        return render_template("error.html", message = "There is no such flight")

    # insert name into the flight
    db.execute("insert into passengers (name, flight_id) values(:name, :flight_id)", {"name":name, "flight_id":flight_id})
    db.commit()

    return render_template("success.html")


@app.route("/flights")
def flights():
    flights = db.execute("select * from flights").fetchall()
    return render_template("flights.html", flights = flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = db.execute("select * from flights where id = :id",{"id":flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message = "There is not such flight")

    passengers = db.execute("select name from passengers where flight_id=:flight_id",
                            {"flight_id":flight_id}).fetchall()

    return render_template("flight.html", flight = flight, passengers = passengers)
