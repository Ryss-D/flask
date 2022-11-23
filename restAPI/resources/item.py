import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items, stores

blp = Blueprint("Items", __name__, description="Operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
        except KeyError:
            abort(404, message="Item not found.")
    
    def put(self, item_id):
        item_data = request.get_json() 
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request, Ensure 'price', and 'name' are included in the JSON payload.")

        try:
            item = items[item_id]
        #|= is a operator that allow us to modificate the value of the 
        #dictionary in place
            item |= item_data
        except KeyError:
         abort(404, message="Item not found.")

    @blp.route("/item")
    class ItemList(MethodView):
        def get(self):
            return {"items": list(items.values())}

        def post(self):
            store_data= request.get_json()
            if "name" not in store_data:
                    abort(
                        400,
            message="Bad request, Ensure 'name' is included in the JSON payload"
        )
            for store in stores.values():
                if store_data["name"] == store["name"]:
            ## 400 bad request, 404 not found
                    abort(400, message=f"{store['name']} already exists")
            store_id = uuid.uuid4().hex
            new_store = {
            **store_data, "id": store_id
            ##**store_data wiil unpack store_data dicotrionary values into de new one
            }
            stores[store_id] = new_store
    ##On response codes 200 represents everything ok
    ##and with 201 code it means evetything ok, i accept your data
            return new_store, 201