# BookReview Backend Project

* [Description](#Description)
* [Required-Technologies](#Required-Technologies)
* [Getting-Started](#Getting-Started)
* [Features](#Features)
* [Instructions](#Instructions)
* [Database-Structure](#Database-Structure)
* [Optional-Resources](#Optional-Resources)
* [Built With](#Built-With)
* [Contributors](#Contributors)
---

## Description
Book Review RESTful CRUD API with protected routes using Python, Flask, SQLalchemy, SQLlite, and JWT.
---

## Required-Technologies
- SQLlite for the database
- Python/Flask to run the application
---

## Getting-Started

### Set-up Project:
1. Clone the project - `git clone https://github.com/Storm-Maker/RESTful_API_BookReview.git`
2. Go into the project directory `./`
3. Install python3.12
4. Install the requirements - `pip install -r requirements.txt`
5. Start the server - `flask run`
6. Create & Migrate DB - `flask db init` then `flask db migrate` then `flask db upgrade`
7. Visit the API Doc - `\swagger-ui`

### Environment Variables:
```
DATABASE_URL        = "sqlite:///data.db"
JWT_SECRET_KEY      = [Password for JWT]
```
---

## Features
1. RESTful CRUD routes for [reviews, books, admin]
2. Protected Routes using JWT
3. API Documentation using Swagger UI

---

## Instructions

### TO connect to the RESTful Routes:

#### Reviews
```
- Index         route: '/reviews'              [GET]
- Show          route: '/reviews/:id'          [GET]
- Create        route: '/reviews'              [POST]
- Update        route: '/reviews/:id'          [PUT]       [Token Required]
- Delete        route: '/reviews/:id'          [DELETE]    [Token Required]
```
#### Books
```
- Index         route: '/books'                [GET]
- Show          route: '/books/:id'            [GET]
- Create        route: '/books'                [POST]
- Update        route: '/books/:id'            [PUT]       [Token Required]
- Delete        route: '/books/:id'            [DELETE]    [Token Required]
```
#### Users
```
- Show          route: '/admin/:id'             [GET]       [Token Required]
- Create        route: '/admin/register'        [POST]
- Delete        route: '/admin/:id'             [DELETE]    [Token Required]
- Login         route: '/admin/login'           [POST]
```
#### API Documentation
```
- Swagger UI    route: '/swagger-ui'
```

---

## Database-Structure

### Models
```
- Reviews
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(100), unique=False, nullable=False)
    rating = db.Column(db.Float(precision=1), unique=False, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), unique=False, nullable=False)
    books = db.relationship("BookModel", back_populates="reviews")

- Books
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(20), unique=False, nullable=False)

    reviews = db.relationship("ReviewModel", back_populates="books", lazy="dynamic", cascade="all, delete")

- Admins
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
```

### Schema
```
class PlainReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    review = fields.Str(required=True)
    rating = fields.Float(required=True, validate=[validate.Range(min=1.0), validate.Range(max=5.0)])


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

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
```

## Optional-Resources

### Postman-Collection
- you can find all the *postman* collection `.json` in 
    `".\Optional\Postman Collection\Books.postman_collection.json"`
    `".\Optional\Postman Collection\Reviews.postman_collection.json"`
    `".\Optional\Postman Collection\Users.postman_collection.json"`
- can be imported using postman application
- you will need to change the Token with a valid token.
---
## Built With
- Python
- Flask
- SQLalchemy
- Marshmallow - Schema
- SQLlite
- Flask Smorest - Blueprints
- Flask Smorest Api - Swagger UI
- Flask Migrate - Alembic
- Flask JWT - Jason Web Token
---
## Contributors
- Mohammed Ahmed Morsi "RESTful API" <stormmaker_cf@hotmail.com>
---
