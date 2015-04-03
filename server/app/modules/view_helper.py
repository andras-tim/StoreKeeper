import re

from flask import request
from marshmallow import Serializer
from sqlalchemy.exc import IntegrityError


def nested_fields(**names_classes):
    """
    Model decorator for pass-trough classes of nested fields
    """
    def class_wrapper(cls):
        setattr(cls, "nested_fields__", names_classes or {})
        return cls
    return class_wrapper


class RequestProcessingError(Exception):
    def __init__(self, message: (str, dict)):
        self.message = message


class PopulateModelOnSubmit(object):
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
            if hasattr(self.__item, "nested_fields__") and name in self.__item.nested_fields__.keys():
                self.__populate_nested_field(name, value, self.__item.nested_fields__[name], field_errors)

            else:
                setattr(self.__item, name, value)

        if field_errors:
            raise RequestProcessingError(field_errors)

    def __populate_nested_field(self, field_name: str, posted_data, nested_class: type, errors: dict):
        """
        Update nested field by its ids
        """
        if type(posted_data) is not dict or "id" not in posted_data.keys():
            errors[field_name] = {"id": "This field is required."}
            return

        nested_id = posted_data["id"]
        nested_object = nested_class.query.get(nested_id)
        if nested_object is None:
            errors[field_name] = {"id": "Referred object is not found."}
            return

        setattr(self.__item, field_name, nested_object)
        return


class SqlErrorParser(object):
    integrity_error_template = re.compile(r"^\(IntegrityError\) (?P<message>.*)$")
    unique_integrity_error_template = re.compile(r"^UNIQUE constraint failed: (?P<table_field>.*)$")
    field_name_template = re.compile(r"^[^.]*\.(?P<field>.*)$")

    @classmethod
    def parse(cls, err: Exception) -> (str, dict):
        raw_message = err.args[0]

        matches = cls.integrity_error_template.search(raw_message)
        if not matches:
            return "Can not commit changes; error=%r" % raw_message
        integrity_error = matches.group("message")

        matches = cls.unique_integrity_error_template.search(integrity_error)
        if not matches:
            return "Can not commit changes; error=%r" % integrity_error
        table_field = matches.group("table_field")

        matches = cls.field_name_template.search(table_field)
        field = table_field
        if matches:
            field = matches.group("field")

        return {field: ['Already exists.']}


def get_validated_request(deserializer: Serializer) -> (dict, list, None):
        json_input = request.get_json()
        if json_input is None:
            raise RequestProcessingError("Validation error; data is non-Json!")

        data, errors = deserializer.load(json_input)
        if errors:
            raise RequestProcessingError(errors)

        return data
