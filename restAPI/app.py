import os 

from flask import Flask, request
from flask_smorest import Api

from db import db
##its the same that use import.__init__
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

##Factory pattern

def create_app(db_url=None):


    #file name and variable name should always be app
    app = Flask(__name__)

    ##if any exceptions occurs inside3 a module
    ##it will propage to the app so we can seeit
    app.config["PROGATE_EXCPETIONS"]=True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    ##SWAGER  adds docmentation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger_ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)


    return app