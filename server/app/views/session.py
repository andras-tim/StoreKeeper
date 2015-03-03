from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user, login_required

from app.forms import SessionCreateForm
from app.models import User
from app.serializers import UserSerializer
from app.server import config, api, bcrypt


class SessionView(restful.Resource):
    @login_required
    def get(self):
        """
        Get current session

        .. http:get:: /api/sessions

            **Example request**:

            .. sourcecode:: http

                GET /storekeeper/api/sessions HTTP/1.1
                Host: localhost:8000
                Content-Type: application/json

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 201 CREATED
                Set-Cookie: session=xxx
                Content-Type: application/json

                {
                    "admin": false,
                    "disabled": false,
                    "email": "foo@bar.com",
                    "id": 1,
                    "username": "foo"
                }

            :resheader Set-Cookie: new session ID for authentication
            :statuscode 201: no error
            :statuscode 401: user was not logged in
        """
        user = User.get_user(g.user.username)
        return UserSerializer(user).data

    def post(self):
        """
        Login user

        .. http:post:: /api/sessions

            **Example request**:

            .. sourcecode:: http

                POST /storekeeper/api/sessions HTTP/1.1
                Host: localhost:8000
                Content-Type: application/json

                {
                    "username": "foo",
                    "password": "pass"
                }

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 201 CREATED
                Set-Cookie: session=xxx
                Content-Type: application/json

                {
                    "admin": false,
                    "disabled": false,
                    "email": "foo@bar.com",
                    "id": 1,
                    "username": "foo"
                }

            :resheader Set-Cookie: new session ID for authentication
            :statuscode 201: no error
            :statuscode 401: user was not logged in
            :statuscode 422: there is missing field
        """
        form = SessionCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User.get_user(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return UserSerializer(user).data, 201
        abort(401)

    @login_required
    def delete(self):
        """
        Logout user

        .. http:delete:: /api/sessions

            **Example request**:

            .. sourcecode:: http

                DELETE /storekeeper/api/sessions HTTP/1.1
                Host: localhost:8000
                Cookie: session=xxx
                Content-Type: application/json

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 200 OK
                Content-Type: application/json

                null

            :reqheader Cookie: session ID to authenticate
            :statuscode 200: no error
            :statuscode 401: user was not logged in
        """
        logout_user()
        return


api.add_resource(SessionView, '/%s/api/sessions' % config.App.NAME, endpoint='sessions')
