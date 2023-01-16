from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integet, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullabe=False)
    ##with sqlalchemy we can explicitly indicate the relation between fields on table
    ##ieg with this foreignkey and where it belongs
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    ##this is like anidated models on dart
    ##backpuulates means taht sotremodel class will also has a item realtion
    ##then will be easy to see the items related with a store
    store = db.relationship("StoreModel", back_populates="items") 
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

