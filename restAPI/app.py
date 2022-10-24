import uuid
from flask import Flask, request
from db import items, stores
from flask_smorest import abort
#file name and variable name should always be app
app = Flask(__name__)


##this is a endpoint definition
#defining get request for server/store location
@app.get("/store")
def get_stores():
    return {"Stores": list(stores.values())}

##JSON IS ALWAYS A STRING!!

#defining post request for server/store location
@app.post("/store")
def create_store():
    ##this convert json string to a python directionary and also request data passed
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

## the <string:name> allowus to pass arguments via url and 
##then use it on function
@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if("price" not in item_data
    or "store_id" not in item_data
    or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request, Ensure 'price', 'store_id', and 'name' are included in the JSON payload",
        )

    for item in item.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, 
            message=f"{item['name']} already existes."
            )

    if item_data["store_id"] not in stores:
        #return {"message":"Store not found"}, 404
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
    ##    return {"message": "Store not found"}, 404
    ##this is a approach using smorest flask
            abort(404, message="Store not found")

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        ##return {"message": "Store not found"}, 404
        abort(404, message="Item not found")
    