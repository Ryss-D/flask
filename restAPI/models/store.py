
from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ##lazy menas taht the items will not fetch from database until
    ##they are needed
    ## with cascade the behavior will pass to delete all the items (childrens) associated if Store(parent) is deleted
    items = db.relationship("ItemModel", back_populates = "store", lazy = "dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy = "dynamic")

