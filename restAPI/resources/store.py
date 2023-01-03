from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchme

## The main aidea behjind blue print in smoret
## is divide an api into multiple segments

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchme)
    def get(self, store_id):
        store = StoreModel.get_or_404(store_id)
        return store


    def delete(self, store_id):
        store = StoreModel.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented")

    
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchme(many=True))
    def get(self):
        ##return {"stores": list(stores.values)}
        return stores.values

    @blp.arguments(StoreSchme)
    @blp.response(201, StoreSchme)
    def post(self, store_data):
            ##** allow us to unpack all arguments paxsed as named arguments
        store = StoreModel(**store_data)
    ##when we create a item id field will hav eno value
            ##until we insert it on db

        try:
                ##add dont writte direct into de db but stage data
            db.session.add(store)
                ##commit writte in db
            db.session.commit()
        except IntegrityError:
            abort(
                400
            , message="A store with that name already exists",
            )
        except SQLAlchemyError:
                abort(500, message= "An error ocurred while inseting the item.")
            
        return store 

