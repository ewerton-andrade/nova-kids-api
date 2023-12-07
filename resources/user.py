from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.user import UserModel
from schemas import UserSchema
from main.utils import hash_pass, query_by_model_field, delete_record_by_field

userStore = Blueprint("UserStore", __name__, description="Operations on users")

@userStore.route("/user/<string:user_email>")
class UserStore(MethodView):
    @jwt_required()
    @userStore.response(200, UserSchema)
    def get(self, user_email):
        try:
            user = query_by_model_field(UserModel, 'username', user_email)
            if user:
                return jsonify({'id': user.id, 'email': user.username, 'profile': user.profile, 'provider': user.provider})
        except:
            abort(404, message="User not found.")

    @jwt_required()
    @userStore.response(200, UserSchema)
    def delete(self, user_email):
        try:
            delete_record_by_field(UserModel, 'username', user_email)
        except:
            abort(404, message="User not found.")


@userStore.route("/users")
class UserList(MethodView):
    @jwt_required()
    @userStore.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @jwt_required()
    @userStore.arguments(UserSchema)
    @userStore.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="This user already exists")
        user = UserModel(**user_data)
        user.password = hash_pass(user.password)
        try:
            db.session.add(user)
            db.session.commit()
            return user, 201
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user")
    
    @jwt_required()
    def put(self, user_email):
        user = UserModel.query.get_or_404(user_email)
        raise NotImplementedError("Updating an user is not implemented.")

    