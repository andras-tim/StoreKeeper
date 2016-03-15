"""
Here are some public functions for API communication

# Notes

Serializers (server => client)
 * all data will pass-trough from model (no type conversion / default value)
 * all serializer fields have to available in data or have to be None

Deserializer (client => server)
 * define all fields with required, validate arguments
 * use `missing` argument for fill up a non-set field with a default value
 * required strings should not be blank
 * use `fields.Nested(<deserializerClass>, only=['id'])` for nested fields
"""
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Regexp
from app.modules.basic_serializer import BasicSerializer


def _not_blank(data):
    if not data:
        raise ValidationError('Missing data for required field.')


def _greater_than_zero(number: (int, float)):
    if not number > 0:
        raise ValidationError('Must be greater than 0.')


def _greater_than_or_equal_zero(number: (int, float)):
    if not number >= 0:
        raise ValidationError('Must be greater than or equal 0.')


class UppercaseString(fields.String):
    def _deserialize(self, *args, **kwargs):
        return super()._deserialize(*args, **kwargs).upper()


class UserSerializer(BasicSerializer):
    fields = ('id', 'username', 'email', 'admin', 'disabled')


class UserDeserializer(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=Regexp(r'^[a-z0-9](|[a-z0-9_.-]*[a-z0-9])$'))
    password = fields.Str(required=True, validate=_not_blank)
    email = fields.Email(required=True)
    admin = fields.Bool()
    disabled = fields.Bool()


class SessionDeserializer(Schema):
    id = fields.Int()
    username = fields.Str(required=True, validate=_not_blank)
    password = fields.Str(required=True, validate=_not_blank)
    remember = fields.Bool(missing=False)


class VendorSerializer(BasicSerializer):
    fields = ('id', 'name')


class VendorDeserializer(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)


class UnitSerializer(BasicSerializer):
    fields = ('id', 'unit')


class UnitDeserializer(Schema):
    id = fields.Int()
    unit = fields.Str(required=True, validate=_not_blank)


class CustomerSerializer(BasicSerializer):
    fields = ('id', 'name')


class CustomerDeserializer(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)


class AcquisitionSerializer(BasicSerializer):
    fields = ('id', 'comment')
    datetime_fields = ('timestamp', )


class AcquisitionDeserializer(Schema):
    id = fields.Int()
    comment = fields.Str()


class StocktakingSerializer(BasicSerializer):
    fields = ('id', 'comment')
    datetime_fields = ('timestamp', 'close_timestamp')
    nested_fields = {
        'close_user': UserSerializer(),
    }


class StocktakingDeserializer(Schema):
    id = fields.Int()
    comment = fields.Str()


class ItemSerializer(BasicSerializer):
    fields = ('id', 'name', 'article_number', 'quantity', 'warning_quantity', 'purchase_price', 'location')
    nested_fields = {
        'vendor': VendorSerializer(),
        'unit': UnitSerializer(),
    }


class ItemDeserializer(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)
    vendor = fields.Nested(VendorDeserializer, required=True, only=['id'])
    article_number = UppercaseString()
    warning_quantity = fields.Float()
    unit = fields.Nested(UnitDeserializer, required=True, only=['id'])
    purchase_price = fields.Float(validate=_greater_than_or_equal_zero)
    location = fields.Str()


class ItemSearchSerializer(Schema):
    type = fields.Str(required=True)
    item_id = fields.Int(required=True)

    name = fields.Str()
    article_number = fields.Str()
    vendor = fields.Str()
    unit = fields.Str()
    master_barcode = fields.Str()

    barcode = fields.Str()
    quantity = fields.Int(default=None)


class ItemBarcodeSerializer(BasicSerializer):
    fields = ('id', 'barcode', 'quantity', 'master', 'main')


class ItemBarcodeDeserializer(Schema):
    id = fields.Int()
    barcode = UppercaseString(validate=_not_blank)
    quantity = fields.Float(validate=_greater_than_zero)
    master = fields.Bool()


class ItemBarcodePrintDeserializer(Schema):
    copies = fields.Int()


class AcquisitionItemSerializer(BasicSerializer):
    fields = ('id', 'quantity')
    nested_fields = {
        'item': ItemSerializer(),
    }


class AcquisitionItemDeserializer(Schema):
    id = fields.Int()
    item = fields.Nested(ItemDeserializer, required=True, only=['id'])
    quantity = fields.Float(required=True, validate=_greater_than_zero)


class StocktakingItemSerializer(BasicSerializer):
    fields = ('id', 'quantity')
    nested_fields = {
        'item': ItemSerializer(),
    }


class StocktakingItemDeserializer(Schema):
    id = fields.Int()
    item = fields.Nested(ItemDeserializer, required=True, only=['id'])
    quantity = fields.Float(required=True)


class BarcodeSerializer(BasicSerializer):
    fields = ('id', 'barcode', 'quantity', 'main', 'master', 'item_id')


class WorkSerializer(BasicSerializer):
    fields = ('id', 'comment')
    datetime_fields = ('outbound_close_timestamp', 'returned_close_timestamp')
    nested_fields = {
        'customer': CustomerSerializer(),
        'outbound_close_user': UserSerializer(),
        'returned_close_user': UserSerializer(),
    }


class WorkDeserializer(Schema):
    id = fields.Int()
    customer = fields.Nested(CustomerDeserializer, required=True, only=['id'])
    comment = fields.Str()


class WorkItemSerializer(BasicSerializer):
    fields = ('id', 'outbound_quantity', 'returned_quantity')
    nested_fields = {
        'item': ItemSerializer()
    }


class WorkItemDeserializer(Schema):
    id = fields.Int()
    item = fields.Nested(ItemDeserializer, required=True, only=['id'])
    outbound_quantity = fields.Float(required=True, validate=_greater_than_zero)
    returned_quantity = fields.Float(validate=_greater_than_or_equal_zero)


class UserConfigSerializer(BasicSerializer):
    fields = ('name', 'value')


class UserConfigDeserializer(Schema):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)
    value = fields.Str(required=True)


class ErrorDeserializer(Schema):
    name = fields.Str()
    message = fields.Str(required=True)
    stack = fields.Str()
    cause = fields.Str()
