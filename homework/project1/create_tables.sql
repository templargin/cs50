CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);

CREATE TABLE books(
  id SERIAL PRIMARY KEY,
  isbn VARCHAR NOT NULL,
  title VARCHAR NOT NULL,
  author VARCHAR NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE reviews(
  id SERIAL PRIMARY KEY,
  rating INTEGER NOT NULL,
  review_text VARCHAR NOT NULL,
  user_id INTEGER REFERENCES users,
  book_id INTEGER REFERENCES books
);