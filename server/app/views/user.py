from app.models import User
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleUsers
from app.serializers import UserSerializer, UserDeserializer
from app.server import config, api
from app.views.common import api_func


def _set_password(user: User):
    if hasattr(user, 'password'):
        user.set_password(user.password)
    return user


class UserModelListView(BaseModelListView):
    _model = User
    _serializer = UserSerializer
    _deserializer = UserDeserializer

    @api_func('List users', url_tail='users',
              admin_required=True,
              response=[ExampleUsers.ADMIN.get(), ExampleUsers.USER1.get()])
    def get(self):
        return self._get()

    @api_func('Create user', url_tail='users',
              admin_required=True,
              request=ExampleUsers.USER1.set(),
              response=ExampleUsers.USER1.get(),
              status_codes={422: 'there is wrong type / missing field, or user is already exist'})
    def post(self):
        user = self._post_populate()
        _set_password(user)
        return self._post_save(user)


class UserView(BaseView):
    _model = User
    _serializer = UserSerializer
    _deserializer = UserDeserializer

    @api_func('Get user', url_tail='users/2',
              response=ExampleUsers.USER1.get(),
              queries={'id': 'ID of selected user'},
              status_codes={404: 'there is no user'})
    def get(self, id: int):
        return self._get(id)

    @api_func('Update user', url_tail='users/2',
              request=ExampleUsers.USER1.set(change={'username': 'new_foo'}),
              response=ExampleUsers.USER1.get(change={'username': 'new_foo'}),
              queries={'id': 'ID of selected user for change'},
              status_codes={403: 'user can not modify another users', 404: 'there is no user'})
    def put(self, id: int):
        user = self._put_populate(id)
        _set_password(user)
        return self._put_save(user)

    @api_func('Delete user', url_tail='users/2',
              admin_required=True,
              response=None,
              queries={'id': 'ID of selected user for delete'},
              status_codes={404: 'there is no user', 422: 'user can not remove itself'})
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(UserModelListView, '/%s/api/users' % config.App.NAME, endpoint='users')
api.add_resource(UserView, '/%s/api/users/<int:id>' % config.App.NAME, endpoint='user')
