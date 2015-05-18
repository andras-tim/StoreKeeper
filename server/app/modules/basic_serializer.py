class BasicSerializer:
    """
    Basic serializer for better performance than marshmallow or restful serializers

    The usage not so clean/user-friendly, but this performs serialization the fastest

    Example:
    >>> class TestSerializer(BasicSerializer):
    ... fields = ('id', 'comment')
    ... datetime_fields = ('timestamp', )
    ... nested_fields = {
    ...     'item': ItemSerializer(),
    ... }
    """
    REST_API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f+00:00'

    fields = ()
    datetime_fields = ()
    nested_fields = {}

    def dump(self, item) -> dict:
        if item is None:
            return self._dump_nones()

        result = dict((name, getattr(item, name)) for name in self.fields)

        for name in self.datetime_fields:
            date = getattr(item, name)
            if date is None:
                result[name] = None
            else:
                result[name] = date.strftime(self.REST_API_DATE_FORMAT)

        for name, serializer in self.nested_fields.items():
            result[name] = serializer.dump(getattr(item, name))

        return result

    def dump_many(self, items) -> list:
        return [self.dump(item) for item in items]

    def _dump_nones(self) -> dict:
        result = dict((name, None) for name in self.fields)

        for name in self.datetime_fields:
            result[name] = None

        for name, serializer in self.nested_fields.items():
            result[name] = serializer.dump(None)

        return result
