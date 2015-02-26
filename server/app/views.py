from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user, current_user, login_required

from app.forms import UserCreateForm, SessionCreateForm, UserUpdateForm
from app.models import User
from app.serializers import UserSerializer
from app.server import app, db, config, api, lm, bcrypt


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    abort(500)


@lm.user_loader
def load_user(unique_id):
    app.logger.debug("load_user: %s" % unique_id)
    return User.query.get(int(unique_id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        app.logger.debug("before_request: user: %s\nauthenticated" % str(g.user))
    else:
        app.logger.debug("before_request: user: %s\nnot authenticated" % str(g.user))


def admin_login_required(func: callable):
    def wrapper(*args, **kwargs):
        if not app.config["TESTING"]:
            if not g.user.is_authenticated():
                abort(401)
            if not g.user.admin:
                abort(403)
        return func(*args, **kwargs)
    return wrapper


class UserListView(restful.Resource):
    @admin_login_required
    def get(self):
        """
        List users (for administrators only)

        .. http:get:: /api/users/

            **Example request**:

            .. sourcecode:: http

                GET /storekeeper/api/users HTTP/1.1
                Host: localhost:8000
                Content-Type: application/json

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 200 OK
                Content-Type: application/json

                [
                    {
                        "admin": true,
                        "disabled": false,
                        "email": "admin@bar.com",
                        "id": 1,
                        "username": "admin"
                    },
                    {
                        "admin": false,
                        "disabled": false,
                        "email": "foo@bar.com",
                        "id": 2,
                        "username": "foo"
                    }
                ]

            :statuscode 200: no error
            :statuscode 401: user was not logged in
            :statuscode 403: user has not enough rights
        """
        users = User.query.all()
        return UserSerializer(users, many=True).data

    @admin_login_required
    def post(self):
        """
        Create user (for administrators only)

        .. http:post:: /api/users/

            **Example request**:

            .. sourcecode:: http

                POST /storekeeper/api/users HTTP/1.1
                Host: localhost:8000
                Content-Type: application/json

                {
                    "username": "foo",
                    "password": "pass",
                    "email": "foo@bar.com"
                }

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 200 OK
                Content-Type: application/json

                {
                    "admin": false,
                    "disabled": false,
                    "email": "foo@bar.com",
                    "id": 1,
                    "username": "foo"
                }

            :statuscode 200: no error
            :statuscode 401: user was not logged in
            :statuscode 403: user has not enough rights
            :statuscode 422: there is missing field, or user is already exist
        """
        form = UserCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User(form.username.data, form.password.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data


class UserView(restful.Resource):
    def get(self, id: int):
        """
        Get user

        .. http:get:: /api/users/(int:id)

            **Example request**:

            .. sourcecode:: http

                GET /storekeeper/api/users/1 HTTP/1.1
                Host: localhost:8000
                Content-Type: application/json

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 200 OK
                Content-Type: application/json

                {
                    "admin": false,
                    "disabled": false,
                    "email": "foo@bar.com",
                    "id": 1,
                    "username": "foo"
                }

            :query id: ID of selected user for change
            :statuscode 201: no error
            :statuscode 404: there is no user
        """
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        return UserSerializer(user).data

    @login_required
    def put(self, id: int):
        """
        Update user (login required)

        .. http:put:: /api/users/(int:id)

            **Example request**:

            .. sourcecode:: http

                PUT /storekeeper/api/users/1 HTTP/1.1
                Host: localhost:8000
                Content-Type: application/json

                {
                    "username": "foo",
                    "password": "pass_new",
                    "email": "foo@bar.com"
                }

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 200 OK
                Set-Cookie: session=xxx
                Content-Type: application/json

                {
                    "admin": false,
                    "disabled": false,
                    "email": "foo@bar.com",
                    "id": 1,
                    "username": "foo"
                }

            :query id: ID of selected user for change
            :resheader Set-Cookie: new session ID for authentication
            :statuscode 201: no error
            :statuscode 401: unauthorized
            :statuscode 404: there is no user
            :statuscode 422: there is missing field
        """
        form = UserUpdateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data

    @admin_login_required
    def delete(self, id: int):
        """
        Delete user (for administrators only)

        .. http:delete:: /api/users/(int:id)

            **Example request**:

            .. sourcecode:: http

                DELETE /storekeeper/api/users/1 HTTP/1.1
                Host: localhost:8000
                Cookie: session=xxx
                Content-Type: application/json

            **Example response**:

            .. sourcecode:: http

                HTTP/1.0 200 OK
                Set-Cookie: session=xxx
                Content-Type: application/json

                null

            :query id: ID of selected user for delete
            :reqheader Cookie: session ID to authenticate
            :resheader Set-Cookie: new session ID for authentication
            :statuscode 200: no error
            :statuscode 401: user was not logged in
            :statuscode 403: user has not enough rights
            :statuscode 404: there is no user
        """
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()
        return


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

api.add_resource(UserListView, '/%s/api/users' % config.App.NAME, endpoint='users')
api.add_resource(UserView, '/%s/api/users/<int:id>' % config.App.NAME, endpoint='user')
api.add_resource(SessionView, '/%s/api/sessions' % config.App.NAME, endpoint='sessions')
