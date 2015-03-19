def common_model(nested_fields: (dict, None)=None):
    def class_wrapper(cls):
        def get(cls, **filter) -> "app.models.XXX":
            """
            Getting record by filter

            :return: class instance
            """
            return cls.query.filter_by(**filter).first()

        def populate_nested_fields(self) -> bool:
            """
            Populate nested fields by theirs ids

            This hack is simplify population of nested fields.

            Original form:
            >>> try:
            >>>    item.vendor = Vendor.get(id=item.vendor["id"])
            >>> except Exception as e:
            >>>    abort(422, message="Missing vendor: %r" % item.vendor)
            >>> try:
            >>>    item...

            New form:
            >>> if not item.populate_nested_fields():
            >>>    abort(422, message=item.populate_errors)

            :param field_name: Name of nested field
            :return: populate was success
            """
            self.populate_errors = {}
            self.populate_errors = {}

            for field_name, nested_class in self.nested_fields__.items():
                posted_data = getattr(self, field_name)
                if type(posted_data) is not dict or "id" not in posted_data.keys():
                    __add_nested_error(self.populate_errors, field_name, "id", "This field is required.")
                    continue

                nested_id = posted_data["id"]
                nested_data = nested_class.get(id=nested_id)
                if nested_data is None:
                    __add_nested_error(self.populate_errors, field_name, "id", "Referred object is not found.")
                    continue

                setattr(self, field_name, nested_data)
            return len(self.populate_errors) == 0

        def __add_nested_error(errors: dict, field_name: str, nested_field_name: str, message: str):
            if field_name not in errors.keys():
                errors[field_name] = {}
            errors[field_name][nested_field_name] = message

        setattr(cls, "nested_fields__", nested_fields or {})
        setattr(cls, "populate_errors", [])

        setattr(cls, "get", classmethod(get))
        setattr(cls, "populate_nested_fields", populate_nested_fields)
        return cls

    return class_wrapper
