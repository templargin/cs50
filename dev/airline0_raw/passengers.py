import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("LOCAL_DB"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    # getting all the flihts
    flights = db.execute("select id, origin, destination, duration from flights").fetchall()
    for flight in flights:
        print(f"Flight {flight.id} : {flight.origin} to {flight.destination}, {flight.duration} minutes.")

    # prompt user to select a flights
    flight_id = int(input("\nChoose a flight number: "))
    flight = db.execute("select origin, destination, duration from flights where id=:id", {"id": flight_id}).fetchone()

    if flight is None:
        print("There is no such flight")

    passengers = db.execute("select name from passengers where flight_id = :flight_id", {"flight_id": flight_id}).fetchall()

    print("\nPassengers:")
    for passenger in passengers:
        print(passenger.name)
    if len(passengers) == 0:
        print("No passengers")


if __name__ == "__main__":
    main()
