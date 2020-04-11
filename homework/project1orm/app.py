import os

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from models import *

from flask_session import Session
#from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from api import get_data_API
from decimal import Decimal
from sqlalchemy.sql import func

app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

# set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("LOCAL_DB_BOOK")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_page")
def login_page():
    if session.get("user") is not None:
        return redirect(url_for('search'))
    return render_template("login.html")

@app.route("/registeration_page")
def registration_page():
    return render_template("register.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template("success.html", message="You have successfully logged out.")


@app.route("/register", methods = ["POST"])
def register():
    username = request.form.get("username")
    user = User.query.filter_by(username = username).first()
    if user is not None:
        return render_template("error.html", message = "Somebody has already taken this username. \nPlease try another one.")

    password = request.form.get("password")

    user = User(username = username, password = password)
    db.session.add(user)
    db.session.commit()

    return render_template("success.html", message = "You have successfully registered.")


@app.route("/search", methods=["POST", "GET"])
def search():

    if session.get("user") is not None:
        return render_template("search.html", from_login = True, user = session["user"])

    username = request.form.get("username")
    password = request.form.get("password")

    #user = db.execute("select * from users where username=:username and password=:password",{"username":username,"password":password}).fetchone()
    user = User.query.filter_by(username = username, password = password).first()

    if user is None:
        return render_template("error.html", message = "Log in with correct username and password.")

    session["user"] = user
    return render_template("search.html", from_login = True, user = session["user"])


@app.route("/search/results", methods = ["POST"])
def search_results():

    search_criteria = request.form.get("search_criteria")
    search_input = request.form.get("search_input")

    #query = "select * from books where " + search_criteria + " like :search_input"
    #books = db.execute(query, {"search_input":'%'+search_input+'%'}).fetchall()

    books = Book.query.filter(getattr(Book, search_criteria).ilike('%'+search_input+'%')).all()

    return render_template("search.html", from_login = False, books = books, search_input = search_input, search_criteria = search_criteria, user = session["user"])

# BOOK DETAILS PAGE
@app.route("/book/<int:book_id>", methods = ["POST" , "GET"])
def book(book_id):
    # Check if user is logged in
    if session.get("user") is None:
        return render_template("error.html", message="Please, log in first.")

    # Make sure book exists
    #book = db.execute("select * from books where id = :book_id", {"book_id":book_id}).fetchone()
    book = Book.query.get(book_id)

    if book is None:
        return render_template("error.html", message = "There is no book with this ID")

    # Submit a reivew to a database
    if request.method == "POST":
        review_text = request.form.get("review_text")
        rating = request.form.get("rating")

        #review = db.execute("select * from reviews where user_id=:user_id and book_id=:book_id", {"user_id":session["user"].id,"book_id":book_id}).fetchone()
        review = Review.query.filter_by(user_id = session["user"].id, book_id = book_id).first()

        if review is not None:
            return render_template("error.html", message = "You have already submitted review for this book.")

        #db.execute("insert into reviews (rating, review_text, user_id, book_id) values (:rating, :review_text, :user_id, :book_id)",{"rating":rating, "review_text":review_text, "book_id":book_id, "user_id":session["user"].id})
        review = Review(rating = rating, review_text = review_text, user_id = session["user"].id, book_id = book_id)
        db.session.add(review)
        db.session.commit()

    # Get reviews from database for this book
    #reviews = db.execute("select * from reviews where book_id=:book_id", {"book_id":book_id}).fetchall()
    reviews = book.reviews

    # Fetch ratings data from Goodreads API
    goodreads_data = get_data_API(book.isbn)

    return render_template("book.html", book = book, reviews = reviews, user = session["user"], goodreads_data = goodreads_data)


# CREATING API
@app.route("/api/<string:isbn>")
def book_api(isbn):
    # Make sure ISBN exists
    #book = db.execute("select * from books where isbn=:isbn", {"isbn":isbn}).fetchone()
    book = Book.query.filter_by(isbn = isbn).first()
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 422


    # Get number of reviews and average rating
    #count = db.execute("select count(*) from reviews where book_id=:book_id",{"book_id":book.id}).fetchone()
    # avg_rating = db.execute("select AVG(rating) from reviews where book_id=:book_id",{"book_id":book.id}).fetchone()

    count = Review.query.filter_by(book_id = book.id).count()
    avg_rating = Review.query.with_entities(func.avg(Review.rating).label('average')).filter(Review.book_id == book.id).first()


    #count = count.count
    if count == 0:
        avg_rating = "N/A"
    else:
        avg_rating = str('{0:.1f}'.format(avg_rating[0]))
        #avg_rating = str(avg_rating[0])

    # Conver to JSON
    return jsonify({
    "ISBN":book.isbn,
    "Title":book.title,
    "Author":book.author,
    "Publication year":book.year,
    "Average rating":avg_rating,
    "Number of reviews":count
    })


if __name__ == "__main__":
    with app.app_context():
        app.run()
