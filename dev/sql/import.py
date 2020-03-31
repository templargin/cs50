import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("LOCAL_DB"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for origin, destination, duration in reader:
        db.execute("insert into flights (origin, destination, duration) values(:origin, :destination, :duration)", {"origin":origin, "destination":destination, "duration":duration})
    db.commit()

if __name__ == "__main__":
    main()
