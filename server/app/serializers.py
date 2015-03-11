from marshmallow import Serializer


class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "username", "email", "admin", "disabled")


class VendorSerializer(Serializer):
    class Meta:
        fields = ("id", "name")


class UnitSerializer(Serializer):
    class Meta:
        fields = ("id", "unit")
