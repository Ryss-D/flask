from marshmallow import Schema, fields

class ItemSchema(Schema):
    ##dump_only means that this field will only 
    ##be returned and cant be passed
    ##by default is false
    ##ieg load_only is the oposite alternative
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=False, required=True)
    price= fields.Float(required=True)
    store_id= fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchme(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
