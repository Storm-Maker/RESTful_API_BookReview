from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ReviewModel
from schemas import ReviewSchema, ReviewUpdateSchema

blp = Blueprint("Reviews", "reviews", description="Reviews Operations")


# reviews root
@blp.route('/reviews')
class ReviewList(MethodView):

    # Post Reviews Endpoint || Create New
    @blp.arguments(ReviewSchema)
    @blp.response(201, ReviewSchema)
    def post(self, review_schema):
        review = ReviewModel(**review_schema)

        try:
            db.session.add(review)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error adding review")

        return review

    # GET All Reviews Endpoint || Retrieve all
    @blp.response(201, ReviewSchema(many=True))
    def get(self):
        return ReviewModel.query.all()


# reviews by ID
@blp.route('/reviews/<int:review_id>')
class Review(MethodView):
    # GET Reviews Endpoint || Retrieve by ID
    @blp.response(200, ReviewSchema)
    def get(self, review_id):
        review = ReviewModel.query.get_or_404(review_id)
        return review

    # Put Reviews Endpoint || Update if exists and create if new
    @jwt_required()
    @blp.arguments(ReviewUpdateSchema)
    @blp.response(201, ReviewSchema)
    def put(self, update_schema, review_id):
        data = ReviewModel.query.get(review_id)

        if data:
            data.review = update_schema["review"]
            data.rating = update_schema["rating"]
        else:
            req_review = ReviewModel(id=review_id, **update_schema)

        db.session.add(data)
        db.session.commit()

        return data

    @jwt_required()
    # Delete Reviews Endpoint || Delete
    def delete(self, review_id):
        review = ReviewModel.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return {"message": f"Review ID: {review_id} is deleted"}
