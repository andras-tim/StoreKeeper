from flask import g
from flask.ext.restful import abort

from app.models import User
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleUsers
from app.serializers import UserSerializer, UserDeserializer
from app.views.common import api_func


def _set_password(user: User):
    if hasattr(user, 'password'):
        user.set_password(user.password)
    return user


class UserListView(BaseModelListView):
    _model = User
    _serializer = UserSerializer
    _deserializer = UserDeserializer

    @api_func('List users', url_tail='/users',
              admin_required=True,
              response=[ExampleUsers.ADMIN.get(), ExampleUsers.USER1.get()])
    def get(self):
        return self._get()

    @api_func('Create user', url_tail='/users',
              admin_required=True,
              request=ExampleUsers.USER1.set(),
              response=ExampleUsers.USER1.get(),
              status_codes={422: '{original} / user is already exist'})
    def post(self):
        user = self._post_populate()
        _set_password(user)
        return self._post_commit(user)


class UserView(BaseView):
    _model = User
    _serializer = UserSerializer
    _deserializer = UserDeserializer

    @api_func('Get user', item_name='user', url_tail='/users/2',
              response=ExampleUsers.USER1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update user', item_name='user', url_tail='/users/2',
              request=ExampleUsers.USER1.set(change={'username': 'new_foo'}),
              response=ExampleUsers.USER1.get(change={'username': 'new_foo'}),
              status_codes={403: 'user can not modify other users', 422: '{original} / user is already exist'})
    def put(self, id: int):
        user = self._put_populate(id)
        if not g.user.admin and not user.id == g.user.id:
            abort(403, message="Can not modify another user")

        _set_password(user)
        return self._put_commit(user)

    @api_func('Delete user', item_name='user', url_tail='/users/2',
              admin_required=True,
              response=None,
              status_codes={403: 'user can not remove itself'})
    def delete(self, id: int):
        user = self._delete_get_item(id)
        if user.id == g.user.id:
            abort(403, message="User can not remove itself")
        return self._delete_commit(user)
