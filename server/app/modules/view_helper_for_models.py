from flask import request
from marshmallow import Serializer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

from app.server import db


def nested_fields(**names_classes):
    """
    Model decorator for pass-trough classes of nested fields
    """
    def class_wrapper(cls):
        setattr(cls, 'nested_fields__', names_classes or {})
        return cls
    return class_wrapper


class RequestProcessingError(Exception):
    def __init__(self, message: (str, dict)):
        self.message = message


class PopulateModelOnSubmit:
    def __init__(self, item, deserializer: Serializer):
        self.__item = item
        self.__deserializer = deserializer

        self.errors = None

    def populate(self) -> bool:
        self.errors = None
        try:
            self.__populate()
        except RequestProcessingError as e:
            self.errors = e.message
            return False
        except IntegrityError as e:
            self.errors = SqlErrorParser.parse(e)
            return False
        return True

    def __populate(self):
        """
        Update item fields by request
        """
        data = get_validated_request(self.__deserializer)

        field_errors = {}
        for name, value in data.items():
            if hasattr(self.__item, 'nested_fields__') and name in self.__item.nested_fields__.keys():
                self.__populate_nested_field(name, value, self.__item.nested_fields__[name], field_errors)

            else:
                setattr(self.__item, name, value)

        if field_errors:
            raise RequestProcessingError(field_errors)

    def __populate_nested_field(self, field_name: str, posted_data, nested_class: type, errors: dict):
        """
        Update nested field by its id
        """
        if type(posted_data) is not dict or 'id' not in posted_data.keys():
            errors[field_name] = {'id': 'This field is required.'}
            return

        nested_id = posted_data['id']
        nested_object = nested_class.query.get(nested_id)
        if nested_object is None:
            errors[field_name] = {'id': 'Referred object is not found.'}
            return

        setattr(self.__item, field_name, nested_object)
        return


class SqlErrorParser:
    @classmethod
    def parse(cls, err: Exception) -> (str, dict):
        raw_message = err.args[0]
        return 'Can not commit changes; error={!r}'.format(raw_message)


def get_validated_request(deserializer: Serializer) -> (dict, list, None):
        json_input = request.get_json()
        if json_input is None:
            raise RequestProcessingError('Validation error; data is non-Json!')

        data, errors = deserializer.load(json_input)
        if errors:
            raise RequestProcessingError(errors)

        return data


class ModelDataDiffer:
    """
    Tool for checking changes of the specified fields
    """
    def __init__(self):
        self.__nested_fields = {}
        self.__original_values = {}

    def save_state(self, model: db.Model):
        self.__initial_enumerate_nested_fields(model)

        self.__original_values = {}
        for column in model.__table__.columns:
            self.__original_values[column.name] = self.__get_field_value(model, column.name)

    def get_diff(self, model: db.Model) -> dict:
        diff = {}

        for column in model.__table__.columns:
            original = self.__original_values[column.name]
            current = self.__get_field_value(model, column.name)
            if original != current:
                diff[column.name] = {'original': original, 'current': current}

        return diff

    def __initial_enumerate_nested_fields(self, model: db.Model):
        if self.__nested_fields:
            return

        relationships = inspect(model.__class__).relationships
        for relationship in relationships:
            nested_field_name = relationship.key
            for local_field, remote_field in relationship.local_remote_pairs:
                self.__nested_fields[local_field.name] = [nested_field_name, remote_field.name]

    def __get_field_value(self, model: db.Model, name: str):
        if name not in self.__nested_fields.keys():
            return getattr(model, name)

        nested_field_name, remote_field_name = self.__nested_fields[name]
        nested_field = getattr(model, nested_field_name)
        return getattr(nested_field, remote_field_name)
