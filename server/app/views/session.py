from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user

from app.forms import SessionCreateForm
from app.models import User
from app.modules.example_data import ExampleUsers
from app.serializers import UserSerializer
from app.server import config, api, bcrypt
from app.views.common import api_func


class SessionView(restful.Resource):
    @api_func("Get current session", url_tail="sessions",
              login_required=True,
              response=ExampleUsers.ADMIN.get())
    def get(self):
        user = User.get_user(g.user.username)
        return UserSerializer(user).data

    @api_func("Login user", url_tail="sessions",
              request=ExampleUsers.ADMIN.set(["username", "password"]),
              response=ExampleUsers.ADMIN.get())
    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User.get_user(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return UserSerializer(user).data, 201
        abort(401)

    @api_func("Logout user", url_tail="sessions",
              login_required=True,
              response=None)
    def delete(self):
        logout_user()
        return


api.add_resource(SessionView, '/%s/api/sessions' % config.App.NAME, endpoint='sessions')
