
from flask import Flask, request
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
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

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)