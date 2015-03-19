def common_model():
    def class_wrapper(cls):
        def get(cls, **filter) -> "app.models.XXX":
            """
            Getting record by filter

            :return: class instance
            """
            return cls.query.filter_by(**filter).first()

        setattr(cls, "get", classmethod(get))
        return cls

    return class_wrapper
