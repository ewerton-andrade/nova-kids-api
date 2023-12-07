import os
import models
from dotenv import load_dotenv
from decouple import config as env
from flask import Flask
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
from resources.user import userStore as UserBlueprint
from main.services import services as ServiceBlueprint
from resources.oauth2 import oauth2 as Oauth2Blueprint
from resources.relatorio import relatorio as RelatorioBlueprint
from main.oauth2 import config_oauth

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():

    app = Flask(__name__)

    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["API_TITLE"] = "Licit API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # app.config["OPENAPI_SWAGGER_UI_URL"] = "https://www.jsdelivr.com/package/npm/swagger-ui-dist"
    app.config["SQLALCHEMY_DATABASE_URI"]=env("DATABASE_URI", "sqlite:///novakids.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["SECRET_KEY"]=env("SECRET_KEY", None)
    app.config["JWT_SECRET_KEY"] = env("JWT_SECRET_KEY", "licit")

    jwt = JWTManager(app)

    jwt_token_exceptions(jwt)
    db_setup(app)

    migrate = Migrate(app, db)
    
    cors_setup(app)
    config_oauth(app)
    api_setup(app)
     
    return app

def db_setup(app, db_url=None):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def cors_setup(app):
    CORS(app, max_age=60*60*4)

def oauth2_setup(app):
    config_oauth(app)

def api_setup(app):
    api = Api(app)
    api.register_blueprint(Oauth2Blueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ServiceBlueprint)
    api.register_blueprint(RelatorioBlueprint)

def jwt_token_exceptions(jwt):
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required"
                }
            ),
            401
        )