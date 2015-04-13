from marshmallow import Serializer, fields, ValidationError
from marshmallow.validate import Regexp

from app.models import *


def _not_blank(data):
    if not data:
        raise ValidationError('Missing data for required field.')


def _greater_than_zero(number: int):
    if not number > 0:
        raise ValidationError('Must be greater than 0.')


class UserSerializer(Serializer):
    class Meta:
        fields = ('id', 'username', 'email', 'admin', 'disabled')


class UserDeserializer(Serializer):
    username = fields.Str(required=True, validate=Regexp(r'^[a-z0-9][a-z0-9_.-]*[a-z0-9]$'))
    password = fields.Str(required=True, validate=_not_blank)
    email = fields.Email(required=True)
    admin = fields.Bool()
    disabled = fields.Bool()


class SessionDeserializer(UserDeserializer):
    class Meta:
        fields = ('username', 'password')


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
    id = fields.Int()
    name = fields.Str(required=True)
    vendor = fields.Nested(VendorSerializer, required=True)
    article_number = fields.Int(default=None)
    quantity = fields.Int(required=True)
    unit = fields.Nested(UnitSerializer, required=True)


class AcquisitionItemSerializer(Serializer):
    id = fields.Int()
    acquisition = fields.Nested(AcquisitionSerializer, required=True)
    item = fields.Nested(ItemSerializer, required=True)
    quantity = fields.Int(required=True, validate=_greater_than_zero)


class StocktakingItemSerializer(Serializer):
    id = fields.Int()
    stocktaking = fields.Nested(StocktakingSerializer, required=True)
    item = fields.Nested(ItemSerializer, required=True)
    quantity = fields.Int(required=True)


class BarcodeSerializer(Serializer):
    id = fields.Int()
    barcode = fields.Str(required=True, validate=_not_blank)
    quantity = fields.Int(validate=_greater_than_zero)
    item = fields.Nested(ItemSerializer, required=True)
    main = fields.Bool()
