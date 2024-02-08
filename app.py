import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from dotenv import load_dotenv

from db import db
import models
from blocklist import BLOCKLIST

# Importing The Blueprints from resources
from resources.books import blp as BooksBlueprint
from resources.reviews import blp as ReviewsBlueprint
from resources.admin import blp as UsersBlueprint


def create_app():
    app = Flask(__name__)

    load_dotenv()

    # Configuring the Blueprints/Routes
    # Flask Config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # Flask Smorest Config
    app.config["API_TITLE"] = "Book Reviews RESTful API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # Swagger UI to display the documentation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # Configuring SQL Alchemy, If no db is defined in env the default will be SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_url", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # Initialize the Flask SQL Alchemy Extension
    db.init_app(app)

    migrate = Migrate(app, db)

    # with app.app_context():
    #     db.create_all()

    # Connect Flask Smorest to FLask App
    api = Api(app)

    # JWT, Dummy password for ease of use change in env with complex.
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "DevPassword")
    jwt = JWTManager(app)

    # Expired JWT
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "Token Revoked", "error": "token_revoked"}), 401

    # JWT Error handling
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The Token has Expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Failed to verify signature", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"description": "Request is missing the access token", "error": "authorization_required"}), 401

    # Registering the blueprints to the api/app
    api.register_blueprint(BooksBlueprint)
    api.register_blueprint(ReviewsBlueprint)
    api.register_blueprint(UsersBlueprint)

    return app
