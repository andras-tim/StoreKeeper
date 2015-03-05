from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_required

from app.forms import UserCreateForm, UserUpdateForm
from app.models import User
from app.serializers import UserSerializer
from app.server import db, config, api
from app.views.common import admin_login_required


class UserListView(restful.Resource):
    @admin_login_required
    def get(self):
        """
        List users (for administrators only)

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
        :statuscode 401: unauthorized
        :statuscode 403: user can not modify another users
        :statuscode 404: there is no user
        :statuscode 422: there is missing field
        """
        if not g.user.admin and id != g.user.id:
            abort(403)

        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        form = UserUpdateForm(obj=user)
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data

    @admin_login_required
    def delete(self, id: int):
        """
        Delete user (for administrators only)

        **Example request**:

        .. sourcecode:: http

            DELETE /storekeeper/api/users/1 HTTP/1.1
            Host: localhost:8000
            Content-Type: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json

            null

        :query id: ID of selected user for delete
        :statuscode 200: no error
        :statuscode 401: user was not logged in
        :statuscode 403: user has not enough rights
        :statuscode 404: there is no user
        :statuscode 422: user can not remove itself
        """

        if id == g.user.id:
            abort(422, message="User can not remove itself")

        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()
        return


api.add_resource(UserListView, '/%s/api/users' % config.App.NAME, endpoint='users')
api.add_resource(UserView, '/%s/api/users/<int:id>' % config.App.NAME, endpoint='user')
