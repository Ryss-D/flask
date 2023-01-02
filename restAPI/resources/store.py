import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchme

## The main aidea behjind blue print in smoret
## is divide an api into multiple segments

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchme)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
    def delete(self, store_id):
        try:
            del stores[store_id] 
            return {"message":"Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

    
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchme(many=True))
    def get(self):
        ##return {"stores": list(stores.values)}
        return stores.values

    @blp.arguments(StoreSchme)
    @blp.response(201, StoreSchme)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store
