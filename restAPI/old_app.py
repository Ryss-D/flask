from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import Flask, request
#file name and variable name should always be app
from flask_smorest import abort

app = Flask(__name__)

stores = [
    {
        "name":"My store",
        "items": [
            {
            "name" : "Chair",
            "price": 15.99
        }
        ]
    }
]

##this is a endpoint definition
#defining get request for server/store location
@app.get("/store")
def get_stores():
    return {"Stores": stores}

##JSON IS ALWAYS A STRING!!

#defining post request for server/store location
@app.post("/store")
def create_store():
    ##this convert json string to a python directionary and also request data passed
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
         "items":[],
    }
    ##On response codes 200 represents everything ok
    ##and with 201 code it means evetything ok, i accept your data
    return new_store, 201

## the <string:name> allowus to pass arguments via url and 
##then use it on function
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item= {
                "name": request_data["name"], 
                "price": request_data["price"],
                }
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404

@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return{store}
    return {"message": "Store not found"}, 404

@app.get("/store/<string:name>/item")
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return{"items": store["items"]}
    return {"message": "Store not found"}, 404
    