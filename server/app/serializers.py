from marshmallow import Serializer


class UserSerializer(Serializer):
    class Meta:
        fields = ("id", "username", "email", "disabled")
