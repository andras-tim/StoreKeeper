from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user

from app.models import User
from app.modules.example_data import ExampleUsers
from app.modules.view_helper_for_models import get_validated_request, RequestProcessingError
from app.serializers import UserSerializer, SessionDeserializer
from app.views.common import api_func


class SessionView(restful.Resource):
    @api_func('Get current session', url_tail='/session',
              response=ExampleUsers.ADMIN.get())
    def get(self):
        user = User.query.filter_by(username=g.user.username).first()
        return UserSerializer(user).data

    @api_func('Login user', url_tail='/session',
              login_required=False,
              request=ExampleUsers.ADMIN.login(),
              response=ExampleUsers.ADMIN.get(),
              status_codes={401: 'bad authentication data or user is disabled'})
    def post(self):
        try:
            data = get_validated_request(SessionDeserializer())
        except RequestProcessingError as e:
            abort(422, message=e.message)

        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            abort(401, message='login error')
        if not login_user(user, remember=data['remember']):
            abort(401, message='login error')
        return UserSerializer(user).data, 201

    @api_func('Logout user', url_tail='/session',
              response=None)
    def delete(self):
        logout_user()
        return
