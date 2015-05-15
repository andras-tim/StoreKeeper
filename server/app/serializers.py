"""
Here are some public functions for API communication

# Notes

Serializers (server => client)
 * use Meta/fields
 * define nested fields, type-extremal defaults (e.g. None) without arguments
 * do not use required=True

Deserializer (client => server)
 * define all fields with required, validate arguments
 * make make_object() for defaults (by default the not set fields the non-present fields)
 * required strings should not be blank

Common
 * nested fields have to refer serializer(!) instance(!)
"""
from marshmallow import Serializer, fields, ValidationError
from marshmallow.validate import Regexp


def _not_blank(data):
    if not data:
        raise ValidationError('Missing data for required field.')


def _greater_than_zero(number: int):
    if not number > 0:
        raise ValidationError('Must be greater than 0.')


def _greater_than_or_equal_zero(number: int):
    if not number >= 0:
        raise ValidationError('Must be greater than or equal 0.')


class UserSerializer(Serializer):
    class Meta:
        fields = ('id', 'username', 'email', 'admin', 'disabled')


class UserDeserializer(Serializer):
    username = fields.Str(required=True, validate=Regexp(r'^[a-z0-9](|[a-z0-9_.-]*[a-z0-9])$'))
    password = fields.Str(required=True, validate=_not_blank)
    email = fields.Email(required=True)
    admin = fields.Bool()
    disabled = fields.Bool()


class SessionDeserializer(Serializer):
    username = fields.Str(required=True, validate=_not_blank)
    password = fields.Str(required=True, validate=_not_blank)
    remember = fields.Bool()

    def make_object(self, data: dict) -> dict:
        if 'remember' not in data.keys():
            data['remember'] = False
        return data


class VendorSerializer(Serializer):
    class Meta:
        fields = ('id', 'name')


class VendorDeserializer(Serializer):
    name = fields.Str(required=True, validate=_not_blank)


class UnitSerializer(Serializer):
    class Meta:
        fields = ('id', 'unit')


class UnitDeserializer(Serializer):
    unit = fields.Str(required=True, validate=_not_blank)


class CustomerSerializer(Serializer):
    class Meta:
        fields = ('id', 'name')


class CustomerDeserializer(Serializer):
    name = fields.Str(required=True, validate=_not_blank)


class AcquisitionSerializer(Serializer):
    comment = fields.Str()

    class Meta:
        fields = ('id', 'timestamp', 'comment')


class AcquisitionDeserializer(Serializer):
    comment = fields.Str()


class StocktakingSerializer(Serializer):
    comment = fields.Str()

    class Meta:
        fields = ('id', 'timestamp', 'comment')


class StocktakingDeserializer(Serializer):
    comment = fields.Str()


class ItemSerializer(Serializer):
    article_number = fields.Int(default=None)
    vendor = fields.Nested(VendorSerializer())
    unit = fields.Nested(UnitSerializer())

    class Meta:
        fields = ('id', 'name', 'vendor', 'article_number', 'quantity', 'unit')


class ItemDeserializer(Serializer):
    name = fields.Str(required=True, validate=_not_blank)
    vendor = fields.Nested(VendorSerializer(), required=True)
    article_number = fields.Int()
    quantity = fields.Int(required=True)
    unit = fields.Nested(UnitSerializer(), required=True)


class AcquisitionItemSerializer(Serializer):
    item = fields.Nested(ItemSerializer())

    class Meta:
        fields = ('id', 'item', 'quantity')


class AcquisitionItemDeserializer(Serializer):
    item = fields.Nested(ItemSerializer(), required=True)
    quantity = fields.Int(required=True, validate=_greater_than_zero)


class StocktakingItemSerializer(Serializer):
    item = fields.Nested(ItemSerializer())

    class Meta:
        fields = ('id', 'item', 'quantity')


class StocktakingItemDeserializer(Serializer):
    item = fields.Nested(ItemSerializer(), required=True)
    quantity = fields.Int(required=True)


class BarcodeSerializer(Serializer):
    item = fields.Nested(ItemSerializer())

    class Meta:
        fields = ('id', 'barcode', 'quantity', 'item', 'main')


class BarcodeDeserializer(Serializer):
    barcode = fields.Str(required=True, validate=_not_blank)
    quantity = fields.Int(validate=_greater_than_zero)
    item = fields.Nested(ItemSerializer(), required=True)
    main = fields.Bool()


class WorkSerializer(Serializer):
    customer = fields.Nested(CustomerSerializer())
    comment = fields.Str()
    outbound_close_user = fields.Nested(UserSerializer())
    returned_close_user = fields.Nested(UserSerializer())

    class Meta:
        fields = ('id', 'customer', 'comment', 'outbound_close_timestamp', 'outbound_close_user',
                  'returned_close_timestamp', 'returned_close_user')


class WorkDeserializer(Serializer):
    customer = fields.Nested(CustomerSerializer(), required=True)
    comment = fields.Str()


class WorkItemSerializer(Serializer):
    item = fields.Nested(ItemSerializer())
    returned_quantity = fields.Int(default=None)

    class Meta:
        fields = ('id', 'item', 'outbound_quantity', 'returned_quantity')


class WorkItemDeserializer(Serializer):
    item = fields.Nested(ItemSerializer(), required=True)
    outbound_quantity = fields.Int(required=True, validate=_greater_than_zero)
    returned_quantity = fields.Int(validate=_greater_than_or_equal_zero)


class ConfigSerializer(Serializer):
    forced_language = fields.Str(default=None)

    class Meta:
        fields = ('app_name', 'app_title', 'forced_language', 'debug')


class UserConfigSerializer(Serializer):
    class Meta:
        fields = ('name', 'value')


class UserConfigDeserializer(Serializer):
    name = fields.Str(required=True, validate=_not_blank)
    value = fields.Str(required=True)
