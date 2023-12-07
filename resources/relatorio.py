from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models.relatorio import RelatorioModel
from schemas import RelatorioSchema
from main.utils import hash_pass, query_by_model_field, delete_record_by_field
from main.oauth2 import require_oauth

relatorio = Blueprint("Relatorio", __name__, description="Operations on users")

@relatorio.route("/relatorio")
class RelatorioList(MethodView):
    # @require_oauth(['admin'])
    # @relatorio.response(200, RelatorioSchema(many=True))
    # def get(self):
    #     return UserModel.query.all()

    # @require_oauth(['admin'])
    @relatorio.arguments(RelatorioSchema)
    @relatorio.response(201, RelatorioSchema)
    def post(self, relatorio_data):
        try:
            relatorio=RelatorioModel(**relatorio_data)
            db.session.add(relatorio)
            db.session.commit()
            return jsonify({"message": "Success"})
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the report")
        # if UserModel.query.filter(UserModel.username == user_data["username"]).first():
        #     abort(409, message="This user already exists")
        # user = UserModel(**user_data)
        # user.password = hash_pass(user.password)
        # try:
        #     db.session.add(user)
        #     db.session.commit()
        #     return user, 201
        # except SQLAlchemyError:
        #     abort(500, message="An error occurred while inserting the user")