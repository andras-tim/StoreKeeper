"""
Here are some public functions for API communication

# Notes

Serializers (server => client)
 * all data will pass-trough from model (no type conversion / default value)
 * all serializer fields have to available in data or have to be None

Deserializer (client => server)
 * define all fields with required, validate arguments
 * make make_object() for defaults (by default the not set fields the non-present fields)
 * required strings should not be blank
 * use deserializer instances(!) in nested fields
"""
from marshmallow import Serializer, fields, ValidationError
from marshmallow.validate import Regexp
from app.modules.basic_serializer import BasicSerializer


def _not_blank(data):
    if not data:
        raise ValidationError('Missing data for required field.')


def _greater_than_zero(number: int):
    if not number > 0:
        raise ValidationError('Must be greater than 0.')


def _greater_than_or_equal_zero(number: int):
    if not number >= 0:
        raise ValidationError('Must be greater than or equal 0.')


class UppercaseString(fields.String):
    def _deserialize(self, value):
        return super()._deserialize(value).upper()


class UserSerializer(BasicSerializer):
    fields = ('id', 'username', 'email', 'admin', 'disabled')


class UserDeserializer(Serializer):
    id = fields.Int()
    username = fields.Str(required=True, validate=Regexp(r'^[a-z0-9](|[a-z0-9_.-]*[a-z0-9])$'))
    password = fields.Str(required=True, validate=_not_blank)
    email = fields.Email(required=True)
    admin = fields.Bool()
    disabled = fields.Bool()


class SessionDeserializer(Serializer):
    id = fields.Int()
    username = fields.Str(required=True, validate=_not_blank)
    password = fields.Str(required=True, validate=_not_blank)
    remember = fields.Bool()

    def make_object(self, data: dict) -> dict:
        if 'remember' not in data.keys():
            data['remember'] = False
        return data


class VendorSerializer(BasicSerializer):
    fields = ('id', 'name')


class VendorDeserializer(Serializer):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)


class UnitSerializer(BasicSerializer):
    fields = ('id', 'unit')


class UnitDeserializer(Serializer):
    id = fields.Int()
    unit = fields.Str(required=True, validate=_not_blank)


class CustomerSerializer(BasicSerializer):
    fields = ('id', 'name')


class CustomerDeserializer(Serializer):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)


class AcquisitionSerializer(BasicSerializer):
    fields = ('id', 'comment')
    datetime_fields = ('timestamp', )


class AcquisitionDeserializer(Serializer):
    id = fields.Int()
    comment = fields.Str()


class StocktakingSerializer(BasicSerializer):
    fields = ('id', 'comment')
    datetime_fields = ('timestamp', )


class StocktakingDeserializer(Serializer):
    id = fields.Int()
    comment = fields.Str()


class ItemSerializer(BasicSerializer):
    fields = ('id', 'name', 'article_number', 'quantity')
    nested_fields = {
        'vendor': VendorSerializer(),
        'unit': UnitSerializer(),
    }


class ItemDeserializer(Serializer):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)
    vendor = fields.Nested(VendorDeserializer(), required=True)
    article_number = UppercaseString()
    quantity = fields.Float(required=True)
    unit = fields.Nested(UnitDeserializer(), required=True)


class ItemBarcodeSerializer(BasicSerializer):
    fields = ('id', 'barcode', 'quantity', 'main')


class ItemBarcodeDeserializer(Serializer):
    id = fields.Int()
    barcode = UppercaseString(validate=_not_blank)
    quantity = fields.Float(validate=_greater_than_zero)
    main = fields.Bool()


class AcquisitionItemSerializer(BasicSerializer):
    fields = ('id', 'quantity')
    nested_fields = {
        'item': ItemSerializer(),
    }


class AcquisitionItemDeserializer(Serializer):
    id = fields.Int()
    item = fields.Nested(ItemDeserializer(), required=True)
    quantity = fields.Float(required=True, validate=_greater_than_zero)


class StocktakingItemSerializer(BasicSerializer):
    fields = ('id', 'quantity')
    nested_fields = {
        'item': ItemSerializer(),
    }


class StocktakingItemDeserializer(Serializer):
    id = fields.Int()
    item = fields.Nested(ItemDeserializer(), required=True)
    quantity = fields.Float(required=True)


class BarcodeSerializer(BasicSerializer):
    fields = ('id', 'barcode', 'quantity', 'main', 'item_id')


class BarcodeDeserializer(Serializer):
    id = fields.Int()
    barcode = fields.Str(required=True, validate=_not_blank)
    quantity = fields.Float(validate=_greater_than_zero)
    item_id = fields.Int(required=True)
    main = fields.Bool()


class WorkSerializer(BasicSerializer):
    fields = ('id', 'comment')
    datetime_fields = ('outbound_close_timestamp', 'returned_close_timestamp')
    nested_fields = {
        'customer': CustomerSerializer(),
        'outbound_close_user': UserSerializer(),
        'returned_close_user': UserSerializer(),
    }


class WorkDeserializer(Serializer):
    id = fields.Int()
    customer = fields.Nested(CustomerDeserializer(), required=True)
    comment = fields.Str()


class WorkItemSerializer(BasicSerializer):
    fields = ('id', 'outbound_quantity', 'returned_quantity')
    nested_fields = {
        'item': ItemSerializer()
    }


class WorkItemDeserializer(Serializer):
    id = fields.Int()
    item = fields.Nested(ItemDeserializer(), required=True)
    outbound_quantity = fields.Float(required=True, validate=_greater_than_zero)
    returned_quantity = fields.Float(validate=_greater_than_or_equal_zero)


class UserConfigSerializer(BasicSerializer):
    fields = ('name', 'value')


class UserConfigDeserializer(Serializer):
    id = fields.Int()
    name = fields.Str(required=True, validate=_not_blank)
    value = fields.Str(required=True)
