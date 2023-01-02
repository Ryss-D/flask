from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    ##dump_only means that this field will only 
    ##be returned and cant be passed
    ##by default is false
    ##ieg load_only is the oposite alternative
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=False, required=True)
    price= fields.Float(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)