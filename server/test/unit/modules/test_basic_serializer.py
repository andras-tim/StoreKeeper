import unittest
import datetime

from app.modules.basic_serializer import BasicSerializer


class NestedData:
    id = 3
    start = datetime.datetime(2014, 5, 6, 17, 18, 19, 432)
    stop = datetime.datetime(2014, 5, 6, 17, 28, 29, 321)


class Data:
    id = 2
    first_name = 'Foo'
    last_name = 'Bar'
    start = datetime.datetime(2000, 1, 2, 13, 14, 15, 678)
    stop = datetime.datetime(2000, 1, 2, 13, 24, 25, 789)
    nested1 = NestedData
    nested2 = NestedData


class TestEmptySerializer(unittest.TestCase):
    class Serializer(BasicSerializer):
        pass

    def test_with_none(self):
        assert {} == self.Serializer().dump(None)

    def test_with_data(self):
        assert {} == self.Serializer().dump(Data)


class TestSerializerWithSomeFields(unittest.TestCase):
    class Serializer(BasicSerializer):
        fields = ('id', 'first_name')

    def test_with_none(self):
        assert {'id': None, 'first_name': None} == self.Serializer().dump(None)

    def test_with_data(self):
        assert {'id': 2, 'first_name': 'Foo'} == self.Serializer().dump(Data)


class TestSerializerWithDatetimeField(unittest.TestCase):
    class Serializer(BasicSerializer):
        datetime_fields = {'start'}

    def test_with_none(self):
        assert {'start': None} == self.Serializer().dump(None)

    def test_with_data(self):
        assert {'start': '2000-01-02T13:14:15.000678+00:00'} == self.Serializer().dump(Data)


class TestSerializerWithNestedField(unittest.TestCase):
    class NestedSerializer(BasicSerializer):
        fields = ('id', )

    class Serializer(BasicSerializer):
        nested_fields = {}

    @classmethod
    def setUpClass(cls):
        cls.Serializer.nested_fields['nested1'] = cls.NestedSerializer()

    def test_with_none(self):
        assert {'nested1': {'id': None}} == self.Serializer().dump(None)

    def test_with_data(self):
        assert {'nested1': {'id': 3}} == self.Serializer().dump(Data)


class TestComplexSerializers(unittest.TestCase):
    class NestedSerializer(BasicSerializer):
        fields = ('id', )
        datetime_fields = ('stop', )

    class Serializer(BasicSerializer):
        fields = ('id', 'last_name')
        datetime_fields = ('start', )
        nested_fields = {}

    @classmethod
    def setUpClass(cls):
        cls.Serializer.nested_fields['nested2'] = cls.NestedSerializer()

    def test_with_none(self):
        assert {'id': None, 'last_name': None, 'start': None,
                'nested2': {'id': None, 'stop': None}} == \
            self.Serializer().dump(None)

    def test_with_data(self):
        assert {'id': 2, 'last_name': 'Bar', 'start': '2000-01-02T13:14:15.000678+00:00',
                'nested2': {'id': 3, 'stop': '2014-05-06T17:28:29.000321+00:00'}} == \
            self.Serializer().dump(Data)
