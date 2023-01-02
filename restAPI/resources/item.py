import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import  ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operation on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    ## this is the default code of response
    ##and will pass whatever be the return
    ##to ItemSchmea
    @blp.response(200, ItemSchema)
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
    
    @blp.arguments(ItemUpdateSchema)
    ##orden of decorator matter
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id ):
        #item_data = request.get_json() 
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
        ##with many=True it auto convert response into a list
        @blp.response(200, ItemSchema(many=True))
        def get(self):
            #return {"items": list(items.values())}
            return items.values()

        ##with this we pass to validation
        ##with marshmallow
        @blp.arguments(ItemSchema)
        ## here the second argument is the json
        ##that pass the validation
        @blp.response(201, ItemSchema)
        def post(self, item_data):
            ##** allow us to unpack all arguments paxsed as named arguments
            item = ItemModel(**item_data)
            ##when we create a item id field will hav eno value
            ##until we insert it on db

            try:
                ##add dont writte direct into de db but stage data
                db.session.add(item)
                ##commit writte in db
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message= "An error ocurred while inseting the item.")
            
            return item