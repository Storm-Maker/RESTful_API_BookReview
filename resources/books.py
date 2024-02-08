from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import BookModel
from schemas import BookSchema, BookUpdateSchema

blp = Blueprint('Books', "books", description="Books Operations")


# Books root
@blp.route('/books')
class BooksList(MethodView):

    # Post Books Endpoint || Create New
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def post(self, book_schema):
        book = BookModel(**book_schema)
        try:
            db.session.add(book)
            db.session.commit()
        except IntegrityError:
            abort(400, message="This Book Title already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the book")

        return book

    # GET All Books Endpoint || Retrieve all
    @blp.response(201, BookSchema(many=True))
    def get(self):
        return BookModel.query.all()


# Books by ID
@blp.route('/books/<int:book_id>')
class Books(MethodView):
    # GET Books Endpoint || Retrieve by ID
    @blp.response(200, BookSchema)
    def get(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        return book

    # Put Books Endpoint || Update if exists and create if new
    @jwt_required()
    @blp.arguments(BookUpdateSchema)
    @blp.response(201, BookSchema)
    def put(self, update_schema, book_id):
        req_book = BookModel.query.get(book_id)
        if req_book:
            req_book.title = update_schema["title"]
            req_book.author = update_schema["author"]
        else:
            req_review = BookModel(id=book_id, **update_schema)

        db.session.add(req_book)
        db.session.commit()

        return req_book

    # Delete Books Endpoint || Delete
    @jwt_required()
    def delete(self, book_id):
        book = BookModel.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": f"Book ID: {book_id} is deleted"}
