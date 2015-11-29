from flask import g
from flask.ext.restful import abort, Resource
from sqlalchemy.exc import IntegrityError

from app.modules.view_helper_for_models import PopulateModelOnSubmit, ModelDataDiffer, SqlErrorParser
from app.server import db
from app.models import User
from app.views.common import commit_with_error_handling, commit_and_rollback_on_error


class BaseView(Resource):
    """
    Model based view

    Example:
    >>> class FooListView(BaseView):
    >>>     _model = Foo
    >>>     _serializer = FooSerializer()
    >>>     _deserializer = FooDeserializer()
    >>>
    >>>     def get(self):
    >>>         return self._get_list()
    >>>
    >>>     def post(self):
    >>>         foo = self._post_populate()
    >>>         # custom changes on model object
    >>>         return self._post_commit(foo)
    >>>
    >>> class FooView(BaseView):
    >>>     _model = Foo
    >>>     _serializer = FooSerializer()
    >>>     _deserializer = FooDeserializer()
    >>>
    >>>     def get(self, id: int):
    >>>         return self._get(id=id)
    >>>
    >>>     def put(self, id: int):
    >>>         foo = self._put_populate(id=id)
    >>>         # custom changes on model object
    >>>         return self._put_commit(foo)
    >>>
    >>>     def delete(self, id: int):
    >>>         return self._delete(id=id)
    """

    _model = None
    _parent_model = None
    _serializer = None
    _deserializer = None
    __differ = ModelDataDiffer()

    @property
    def _current_user(self) -> User:
        return g.user

    def _get_list(self, **filter) -> 'RPC response':
        """
        List model objects
        """
        model_objects = self._model.query.filter_by(**filter)
        return self.__serialize_many(model_objects)

    def _get(self, **filter) -> 'RPC response':
        """
        Single model object getter
        """
        model_object = self._get_model_object(**filter)
        return self.__serialize(model_object)

    def _post(self, **filter) -> 'RPC response':
        """
        Save new model object in one command

        Same as:
        >>> model_object = self._post_populate()
        >>> return self._post_commit(model_object)
        """
        model_object = self._post_populate(**filter)
        return self._post_commit(model_object)

    def _post_retryable_commit(self, model_object_generator: callable, retry_count: int=10) -> 'RPC response':
        """
        Generate a new model object and try to save (trying, because want to skip collision)
        """
        last_exception = None
        for retried_count in range(retry_count):
            model_object = model_object_generator()
            db.session.add(model_object)
            try:
                commit_and_rollback_on_error(db)
                return self.__serialize(model_object)
            except IntegrityError as e:
                last_exception = e
        return abort(422, message='Can not generate unique model object; {}'.format(
            SqlErrorParser.parse(last_exception)
        ))

    def _put(self, **filter) -> 'RPC response':
        """
        Change single model object in one command

        Same as:
        >>> model_object = self._put_populate()
        >>> return self._put_commit(model_object)
        """
        model_object = self._put_populate(**filter)
        return self._put_commit(model_object)

    def _delete(self, **filter) -> 'RPC response':
        """
        Delete single model object in one command

        Same as:
        >>> model_object = self._delete_get_model_object()
        >>> return self._delete_commit(model_object)
        """
        model_object = self._delete_get_model_object(**filter)
        return self._delete_commit(model_object)

    def _post_populate(self, **set_fields) -> 'model object':
        """
        Populate a new model object
        """
        model_object = self._model()
        for name, value in set_fields.items():
            setattr(model_object, name, value)
        self.__populate_model_object(model_object)
        return model_object

    def _post_commit(self, model_object) -> 'RPC response':
        """
        Save the new model object
        """
        db.session.add(model_object)
        commit_with_error_handling(db)
        return self.__serialize(model_object)

    def _put_populate(self, **filter) -> 'model object':
        """
        Populate change model object
        """
        model_object = self._get_model_object(**filter)
        self.__populate_model_object(model_object)
        return model_object

    def _put_commit(self, model_object) -> 'RPC response':
        """
        Save change model object
        """
        commit_with_error_handling(db)
        return self.__serialize(model_object)

    def _delete_get_model_object(self, **filter) -> 'model object':
        """
        Getting model object for delete
        """
        return self._get_model_object(**filter)

    def _delete_commit(self, model_object) -> None:
        """
        Commit model object delete
        """
        db.session.delete(model_object)
        commit_with_error_handling(db)
        return None

    def _apply_quantity_changes(self, nested_model_objects: list, insufficient_quantity_error_message: str,
                                quantity_field_of_object: str= 'quantity', multiplier_for_sign: int=1):
        """
        Pre-check and apply quantity changes
        """
        insufficient_quantities = []

        for nested_model_object in nested_model_objects:
            quantity = getattr(nested_model_object, quantity_field_of_object)
            if quantity is None:
                continue

            quantity_diff = multiplier_for_sign * quantity
            if nested_model_object.item.quantity + quantity_diff < 0:
                insufficient_quantities.append(nested_model_object)
                continue

            nested_model_object.item.quantity += quantity_diff

        if insufficient_quantities:
            db.session.rollback()
            abort(422, message='{}: {}'.format(insufficient_quantity_error_message, ', '.join(
                ['{name!r}: {current} - {decrease}'.format(
                    name=model_item.item.name,
                    current=model_item.item.quantity,
                    decrease=-multiplier_for_sign * getattr(model_item, quantity_field_of_object)
                ) for model_item in insufficient_quantities]
            )))

        commit_with_error_handling(db)

    def _call_with_handle_errors(self, model_function: callable, *args, **kwargs):
        try:
            model_function(*args, **kwargs)
        except RuntimeError as e:
            abort(422, message=e.args[0])

    def _get_model_object(self, **filter) -> 'model object':
        model_object = self._model.query.filter_by(**filter).scalar()
        self.__check_is_missing(model_object)
        return model_object

    def _initialize_parent_model_object(self, parent_id: int) -> 'model object':
        model_object = self._parent_model.query.get(parent_id)
        self.__check_is_missing(model_object)
        return model_object

    def __populate_model_object(self, model_object):
        p = PopulateModelOnSubmit(model_object, self._deserializer)
        if not p.populate():
            abort(422, message=p.errors)

    def __serialize(self, model_object) -> dict:
        return self._serializer.dump(model_object)

    def __serialize_many(self, model_objects) -> list:
        return self._serializer.dump_many(model_objects)

    def __check_is_missing(self, model_object):
        if not model_object:
            abort(404)

    def _save_original_before_populate(self, model_object):
        self.__differ.save_state(model_object)

    def _get_populate_diff(self, model_object) -> dict:
        return self.__differ.get_diff(model_object)
