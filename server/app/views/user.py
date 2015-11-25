from flask import g
from flask.ext.restful import abort

from app.models import User, UserConfig
from app.views.base_views import BaseListView, BaseView
from app.modules.example_data import ExampleUsers, ExampleUserConfigs
from app.serializers import UserSerializer, UserDeserializer, UserConfigSerializer, UserConfigDeserializer
from app.views.common import api_func


def _set_password(user: User):
    if hasattr(user, 'password'):
        user.set_password(user.password)
    return user


class UserListView(BaseListView):
    _model = User
    _serializer = UserSerializer()
    _deserializer = UserDeserializer()

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
    _serializer = UserSerializer()
    _deserializer = UserDeserializer()

    @api_func('Get user', item_name='user', url_tail='/users/2',
              response=ExampleUsers.USER1.get())
    def get(self, id: int):
        return self._get(id=id)

    @api_func('Update user', item_name='user', url_tail='/users/2',
              request=ExampleUsers.USER1.set(change={'username': 'new_foo'}),
              response=ExampleUsers.USER1.get(change={'username': 'new_foo'}),
              status_codes={403: 'user can not modify other users', 422: '{original} / user is already exist'})
    def put(self, id: int):
        user = self._put_populate(id=id)
        if not g.user.admin and not user.id == g.user.id:
            abort(403, message="Can not modify another user")

        _set_password(user)
        return self._put_commit(user)

    @api_func('Delete user', item_name='user', url_tail='/users/2',
              admin_required=True,
              response=None,
              status_codes={403: 'user can not remove itself'})
    def delete(self, id: int):
        user = self._delete_get_item(id=id)
        if user.id == g.user.id:
            abort(403, message="User can not remove itself")
        return self._delete_commit(user)


class UserConfigListView(BaseListView):
    _model = UserConfig
    _parent_model = User
    _serializer = UserConfigSerializer()
    _deserializer = UserConfigDeserializer()

    @api_func('List user items.', url_tail='/users/2/config',
              response=[ExampleUserConfigs.CONFIG1.get(), ExampleUserConfigs.CONFIG2.get()],
              queries={'id': 'ID of user'})
    def get(self, id: int):
        self._initialize_parent_item(id)
        return self._get(user_id=id)

    @api_func('Create user item', url_tail='/users/2/config',
              request=ExampleUserConfigs.CONFIG1.set(),
              response=ExampleUserConfigs.CONFIG1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of user'})
    def post(self, id: int):
        self._initialize_parent_item(id)
        return self._post(user_id=id)


class UserConfigView(BaseView):
    _model = UserConfig
    _parent_model = User
    _serializer = UserConfigSerializer()
    _deserializer = UserConfigDeserializer()

    @api_func('Get user item', item_name='user item', url_tail='/users/2/config/lang',
              response=ExampleUserConfigs.CONFIG1.get(),
              queries={'id': 'ID of user',
                       'name': 'Name of selected user config value for get'})
    def get(self, id: int, name: str):
        self._initialize_parent_item(id)
        return self._get(user_id=id, name=name)

    @api_func('Update user item', item_name='user item', url_tail='/users/2/config/lang',
              request=ExampleUserConfigs.CONFIG1.set(),
              response=ExampleUserConfigs.CONFIG1.get(),
              status_codes={422: '{{ original }} / can not use one config name twice'},
              queries={'id': 'ID of user',
                       'name': 'Name of selected user config value for put'})
    def put(self, id: int, name: str):
        self._initialize_parent_item(id)
        return self._put(user_id=id, name=name)

    @api_func('Delete user item', item_name='user item', url_tail='/users/2/config/lang',
              response=None,
              queries={'id': 'ID of user',
                       'name': 'Name of selected user config value for delete'})
    def delete(self, id: int, name: str):
        self._initialize_parent_item(id)
        return self._delete(user_id=id, name=name)
