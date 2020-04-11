from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    reviews = db.relationship("Review", backref = "user", lazy=True)

    def add_review(self, user_id, book_id, rating, review_text):
        review = Review(user_id = self.id, book_id = book_id, rating = rating, review_text = review_text)
        db.session.add(review)
        db.session.commit()

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    reviews = db.relationship("Review", backref = "book", lazy=True)

    def add_review(self, user_id, book_id, rating, review_text):
        review = Review(user_id = user_id, book_id = self.id, rating = rating, review_text = review_text)
        db.session.add(review)
        db.session.commit()

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable = False)
    review_text = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)
