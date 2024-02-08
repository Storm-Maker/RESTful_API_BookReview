from db import db


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(20), unique=False, nullable=False)

    reviews = db.relationship("ReviewModel", back_populates="books", lazy="dynamic", cascade="all, delete")
