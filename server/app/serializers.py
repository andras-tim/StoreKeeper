from marshmallow import Serializer, fields


class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "username", "email", "admin", "disabled")


class VendorSerializer(Serializer):
    class Meta:
        fields = ("id", "name")


class UnitSerializer(Serializer):
    class Meta:
        fields = ("id", "unit")


class CustomerSerializer(Serializer):
    class Meta:
        fields = ("id", "name")


class AcquisitionSerializer(Serializer):
    comment = fields.Str()
    # TODO: items = fields.Nested(AcquisitionItemSerializer)

    class Meta:
        fields = ("id", "timestamp", "comment")
