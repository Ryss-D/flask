from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import  ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operation on items")
##blue prinrt recives positional and named argments
#the two positional refer to de name of the blue print and the import name of the argument
##name (str) – The name of the blueprint. Will be prepended to each endpoint name.
##import_name (str) – The name of the blueprint package, usually __name__. This helps locate the root_path for the blueprint.
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    ## this is the default code of response
    ##and will pass whatever be the return
    ##to ItemSchmea
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        ##this i only avaliable with flask sqlarchemy, with vanilla alchemy we will have to find other way
        ##get or 404 use the primary key to search
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message= "Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item has been delted"}, 200
    
    @jwt_required()
    ## this is all the implementation needed to 
    ##implement security via jwt to a spcifid endpoint
    ## as defaul on header must go 
    ## Autorization Bearer $JWT
    ##Bearer means "Portador"
    ##Bearer is like a convention
    @blp.arguments(ItemUpdateSchema)
    ##To inject arguments into a view function, use the Blueprint.arguments decorator. It allows to specify a Schema to deserialize and validate the parameters.
##When processing a request, the input data is deserialized, validated, and injected in the view function.
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
            return ItemModel.query.all()

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