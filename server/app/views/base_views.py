from flask.ext import restful
from flask.ext.restful import abort
from sqlalchemy.orm import Query

from app.modules.view_helper_for_models import PopulateModelOnSubmit, ModelDataDiffer
from app.server import db
from app.views.common import commit_with_error_handling


class _BaseModelResource(restful.Resource):
    _model = None
    _serializer = None
    _deserializer = None

    @property
    def _query(self) -> Query:
        return self._model.query

    def _populate_item(self, item):
        p = PopulateModelOnSubmit(item, self._deserializer)
        if not p.populate():
            abort(422, message=p.errors)

    def _serialize(self, item) -> dict:
        return self._serializer.dump(item)

    def _serialize_many(self, items) -> list:
        return self._serializer.dump_many(items)


class BaseListView(_BaseModelResource):
    """
    Model based list view

    Example:
    >>> class FooListView(BaseListView):
    >>>     _model = Foo
    >>>     _serializer = FooSerializer()
    >>>     _deserializer = FooDeserializer()
    >>>
    >>>     def get(self):
    >>>         return self._get()
    >>>
    >>>     def post(self):
    >>>         foo = self._post_populate()
    >>>         # custom changes on object
    >>>         return self._post_commit(foo)
    """

    def _get(self) -> 'RPC response':
        """
        List items
        """
        items = self._query.all()
        return self._serialize_many(items)

    def _post(self) -> 'RPC response':
        """
        Save new item in one command

        Same as:
        >>> item = self._post_populate()
        >>> return self._post_commit(item)
        """
        item = self._post_populate()
        return self._post_commit(item)

    def _post_populate(self) -> 'item':
        """
        Populate a new object
        """
        item = self._model()
        self._populate_item(item)
        return item

    def _post_commit(self, item) -> 'RPC response':
        """
        Save the new object
        """
        db.session.add(item)
        commit_with_error_handling(db)
        return self._serialize(item)


class BaseView(_BaseModelResource):
    """
    Model based view

    Example:
    >>> class FooView(BaseView):
    >>>     _model = Foo
    >>>     _serializer = FooSerializer()
    >>>     _deserializer = FooDeserializer()
    >>>
    >>>     def get(self, id: int):
    >>>         return self._get(id)
    >>>
    >>>     def put(self, id: int):
    >>>         foo = self._put_populate(id)
    >>>         # custom changes on object
    >>>         return self._put_commit(foo)
    >>>
    >>>     def delete(self, id: int):
    >>>         return self._delete(id)
    """

    def _get(self, id: int) -> 'RPC response':
        """
        Single item getter
        """
        item = self._get_item_by_id(id)
        return self._serialize(item)

    def _put(self, id: int) -> 'RPC response':
        """
        Change single item in one command

        Same as:
        >>> item = self._put_populate()
        >>> return self._put_commit(item)
        """
        item = self._put_populate(id)
        return self._put_commit(item)

    def _delete(self, id: int) -> 'RPC response':
        """
        Delete single item in one command

        Same as:
        >>> item = self._delete_get_item()
        >>> return self._delete_commit(item)
        """
        item = self._delete_get_item(id)
        return self._delete_commit(item)

    def _put_populate(self, id: int) -> 'item':
        """
        Populate change object
        """
        item = self._get_item_by_id(id)
        self._populate_item(item)
        return item

    def _put_commit(self, item) -> 'RPC response':
        """
        Save change object
        """
        commit_with_error_handling(db)
        return self._serialize(item)

    def _delete_get_item(self, id: int) -> 'item':
        """
        Getting object for delete
        """
        return self._get_item_by_id(id)

    def _delete_commit(self, item) -> None:
        """
        Commit item delete
        """
        db.session.delete(item)
        commit_with_error_handling(db)
        return None

    def _get_item_by_id(self, id: int) -> 'item':
        item = self._query.get(id)
        _check_is_missing(item)
        return item


class BaseNestedListView(BaseListView):
    _parent_model = None

    def _get(self, **filter) -> 'RPC response':
        """
        List items
        """
        items = self._query.filter_by(**filter)
        return self._serialize_many(items)

    def _post(self, **filter) -> 'RPC response':
        """
        Save new item in one command

        Same as:
        >>> item = self._post_populate()
        >>> return self._post_commit(item)
        """
        item = self._post_populate(**filter)
        return self._post_commit(item)

    def _post_populate(self, **set_fields) -> 'item':
        """
        Populate a new object
        """
        item = self._model()
        for name, value in set_fields.items():
            setattr(item, name, value)
        self._populate_item(item)
        return item

    def _initialize_parent_item(self, parent_id: int) -> 'item':
        return _initialize_parent_item(self._parent_model, parent_id)


class BaseNestedModelView(BaseView):
    _parent_model = None

    def _get(self, **filter) -> 'RPC response':
        """
        Single item getter
        """
        item = self._get_item_by_filter(**filter)
        return self._serialize(item)

    def _put(self, **filter) -> 'RPC response':
        """
        Change single item in one command

        Same as:
        >>> item = self._put_populate()
        >>> return self._put_commit(item)
        """
        item = self._put_populate(**filter)
        return self._put_commit(item)

    def _delete(self, **filter) -> 'RPC response':
        """
        Delete single item in one command

        Same as:
        >>> item = self._delete_get_item()
        >>> return self._delete_commit(item)
        """
        item = self._delete_get_item(**filter)
        return self._delete_commit(item)

    def _put_populate(self, **filter) -> 'item':
        """
        Populate change object
        """
        item = self._get_item_by_filter(**filter)
        self._populate_item(item)
        return item

    def _delete_get_item(self, **filter) -> 'item':
        """
        Getting object for delete
        """
        return self._get_item_by_filter(**filter)

    def _get_item_by_filter(self, **filter) -> 'item':
        item = self._query.filter_by(**filter).first()
        _check_is_missing(item)
        return item

    def _initialize_parent_item(self, parent_id: int) -> 'item':
        return _initialize_parent_item(self._parent_model, parent_id)


class BaseNestedModelViewWithDiff(BaseNestedModelView):
    __differ = ModelDataDiffer()

    def _save_original_before_populate(self, id: int):
        self.__differ.save_state(self._get_item_by_id(id))

    def _get_populate_diff(self, item) -> dict:
        return self.__differ.get_diff(item)


def _check_is_missing(item):
    if not item:
        abort(404)


def _initialize_parent_item(parent_model, parent_id: int) -> 'item':
    item = parent_model.query.get(parent_id)
    _check_is_missing(item)
    return item
