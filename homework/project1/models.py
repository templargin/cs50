class User:
    counter = 1
    def __init__(self, username, password):
        self.id = counter
        counter += 1
        self.username = username
        self.password = password
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

class Book:
    counter = 1
    def __init__(self, isbn, title, author, year):
        self.id = counter
        counter += 1
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.review_count =  0
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)
        self.review_count += 1

class Review:
    counter = 1
    def __init__(self, user_id, book_id, rating, review_text):
        self.id = counter
        counter += 1
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.review_text = review_text
