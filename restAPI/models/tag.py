from db import db

class TagModel(db.Model):
    __tablename_= "tags"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer(), db.ForeigKey("stores.id"), nollable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")