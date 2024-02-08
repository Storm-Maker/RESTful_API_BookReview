from marshmallow import Schema, fields, validate


class PlainReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    review = fields.Str(required=True)
    rating = fields.Float(required=True, validate=[validate.Range(min=1.0), validate.Range(max=5.0)])

    # @validates_schema
    # def validate_rating(self, rating):
    #     if rating > 5.0 or rating < 1.0:
    #         return ValidationError('Rating must be between 1.0 to 5.0')


class PlainBookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)


class ReviewSchema(PlainReviewSchema):
    book_id = fields.Int(required=True, load_only=True)
    book = fields.Nested(PlainBookSchema(), dumb_only=True)


class ReviewUpdateSchema(Schema):
    review = fields.Str()
    rating = fields.Float(validate=[validate.Range(min=1.0), validate.Range(max=5.0)])
    book_id = fields.Int()


class BookUpdateSchema(Schema):
    title = fields.Str()
    author = fields.Str()


class BookSchema(PlainBookSchema):
    reviews = fields.List(fields.Nested(PlainReviewSchema()), dumb_only=True)


# User Schema and not Admin Schema cuz it should work for both in the future.
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    # Password is load only so it won't be returned from API.
    password = fields.Str(required=True, load_only=True)
