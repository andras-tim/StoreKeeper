from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user

from app.forms import SessionCreateForm
from app.models import User
from app.modules.example_data import ExampleUsers
from app.serializers import UserSerializer
from app.server import config, api
from app.views.common import api_func


class SessionView(restful.Resource):
    @api_func("Get current session", url_tail="sessions",
              response=ExampleUsers.ADMIN.get())
    def get(self):
        user = User.get(username=g.user.username)
        return UserSerializer(user).data

    @api_func("Login user", url_tail="sessions",
              login_required=False,
              request=ExampleUsers.ADMIN.set(["username", "password"]),
              response=ExampleUsers.ADMIN.get(),
              status_codes={401: "bad authentication data or user is disabled",
                            422: "there is wrong type / missing field"})
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User.get(username=form.username.data)
        if not user or not user.check_password(form.password.data):
            abort(401)
        if not login_user(user):
            abort(401)
        return UserSerializer(user).data, 201

    @api_func("Logout user", url_tail="sessions",
              response=None)
    def delete(self):
        logout_user()
        return


api.add_resource(SessionView, '/%s/api/sessions' % config.App.NAME, endpoint='sessions')
