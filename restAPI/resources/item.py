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
        ##this i only avaliable with flask sqlarchemy, with vanilla alchemy we will have to find other way
        ##get or 404 use the primary key to search
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented.")
    
    @blp.arguments(ItemUpdateSchema)
    ##orden of decorator matter
    @blp.response(200, ItemSchema)
    ##put request should have the same state at the end independly if we receive one o ten time the request
    ##ieg if a user push multiple times a button of send by mistake two times the same request
    def put(self,item_data, item_id ):
        item = ItemModel.query.get(item_id)
        ## item will be true if item exists 
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        raise NotImplementedError("Updating an item is not implemented.")

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