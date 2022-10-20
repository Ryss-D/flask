import uuid
from flask import Flask, request
from db import items, stores
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
    if item_data["store_id"] not in stores:
        return {"message":"Store not found"}, 404

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
        return {"message": "Store not found"}, 404

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Store not found"}, 404
    