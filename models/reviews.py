from db import db


class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(100), unique=False, nullable=False)
    rating = db.Column(db.Float(precision=1), unique=False, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), unique=False, nullable=False)
    books = db.relationship("BookModel", back_populates="reviews")
