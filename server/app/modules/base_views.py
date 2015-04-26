from flask.ext import restful
from flask.ext.restful import abort

from app.modules.view_helper import PopulateModelOnSubmit, ModelDataDiffer
from app.server import db
from app.views.common import commit_with_error_handling


class _BaseModelResource(restful.Resource):
    _model = None
    _serializer = None
    _deserializer = None

    def _populate_item(self, item):
        p = PopulateModelOnSubmit(item, self._deserializer())
        if not p.populate():
            abort(422, message=p.errors)


class BaseModelListView(_BaseModelResource):
    """
    Model based list view

    Example:
    >>> class FooListView(BaseModelListView):
    >>>     _model = Foo
    >>>     _serializer = FooSerializer
    >>>     _deserializer = FooDeserializer
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
        items = self._model.query.all()
        return self._serializer(items, many=True).data

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
        return self._serializer(item).data


class BaseView(_BaseModelResource):
    """
    Model based view

    Example:
    >>> class FooView(BaseView):
    >>>     _model = Foo
    >>>     _serializer = FooSerializer
    >>>     _deserializer = FooDeserializer
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
        return self._serializer(item).data

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
        item = self._get_item_by_id(id)

        db.session.delete(item)
        commit_with_error_handling(db)
        return None

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
        return self._serializer(item).data

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
        item = self._model.query.get(id)
        if not item:
            abort(404)
        return item


class BaseViewWithDiff(BaseView):
    __differ = ModelDataDiffer()

    def _save_original_before_populate(self, id: int):
        self.__differ.save_state(self._get_item_by_id(id))

    def _get_populate_diff(self, item) -> dict:
        return self.__differ.get_diff(item)
