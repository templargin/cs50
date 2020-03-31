import os
import csv

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("LOCAL_DB")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    flights = Flight.query.filter(Flight.duration < 500).all()
    for flight in flights:
        print(f"{flight.origin} to {flight.destination}, {flight.duration}")


if __name__ == "__main__":
    with app.app_context():
        main()
