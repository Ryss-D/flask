from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    ##dump_only means that this field will only 
    ##be returned and cant be passed
    ##by default is false
    ##ieg load_only is the oposite alternative
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=False, required=True)
    price= fields.Float(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagScheme(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)



class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagScheme()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tag = fields.List(fields.Nested(PlainTagScheme()), dump_only=True)

class TagSchema(PlainTagScheme):
    store_id = fields.Int(load_only=True)
    stores = fields.List(fields.Nested(PlainStoreSchema()), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema), dump_only = True)

class TagAndItemSchema(Schema):
    message= fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)