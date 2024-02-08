from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from blocklist import BLOCKLIST
from db import db
from models import AdminModel
from schemas import UserSchema

blp = Blueprint("Admins", "admins", description="Admin Operations")


@blp.route("/admin/register")
class AdminRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if AdminModel.query.filter(AdminModel.username == user_data["username"]).first():
            abort(409, message="Username already exists")

        # User Password is hashed into db using passlib
        user = AdminModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "User Created"}, 201


@blp.route("/admin/login")
class AdminLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = AdminModel.query.filter(AdminModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            user_token = create_access_token(identity=user.id)
            return {"token": user_token}, 200

        abort(401, message="Invalid Credentials, Check Username and Password")


@blp.route("/admin/logout")
class AdminLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out"}


@blp.route("/admin/<int:user_id>")
class Admin(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = AdminModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = AdminModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User Deleted"}, 200
