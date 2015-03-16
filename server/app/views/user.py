from flask import g
from flask.ext import restful
from flask.ext.restful import abort

from app.forms import UserCreateForm, UserUpdateForm
from app.models import User
from app.modules.example_data import ExampleUsers
from app.serializers import UserSerializer
from app.server import db, config, api
from app.views.common import api_func


class UserListView(restful.Resource):
    @api_func("List users", url_tail="users",
              admin_required=True,
              response=[ExampleUsers.ADMIN.get(), ExampleUsers.USER1.get()])
    def get(self):
        users = User.query.all()
        return UserSerializer(users, many=True).data

    @api_func("Create user", url_tail="users",
              admin_required=True,
              request=ExampleUsers.USER1.set(),
              response=ExampleUsers.USER1.get(),
              status_codes={422: "there is wrong type / missing field, or user is already exist"})
    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User(username=form.username.data, email=form.email.data, admin=form.admin.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data


class UserView(restful.Resource):
    @api_func("Get user", url_tail="users/2",
              response=ExampleUsers.USER1.get(),
              queries={"id": "ID of selected user"},
              status_codes={404: "there is no user"})
    def get(self, id: int):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        return UserSerializer(user).data

    @api_func("Update user", url_tail="users/2",
              request=ExampleUsers.USER1.set(change={"username": "new_foo"}),
              response=ExampleUsers.USER1.get(change={"username": "new_foo"}),
              queries={"id": "ID of selected user for change"},
              status_codes={403: "user can not modify another users", 404: "there is no user"})
    def put(self, id: int):
        if not g.user.admin and id != g.user.id:
            abort(403)

        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        form = UserUpdateForm(obj=user)
        if not form.validate_on_submit():
            abort(422, message=form.errors)
        user.set_password(form.password.data)

        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data

    @api_func("Delete user", url_tail="users/2",
              admin_required=True,
              response=None,
              queries={"id": "ID of selected user for delete"},
              status_codes={404: "there is no user", 422: "user can not remove itself"})
    def delete(self, id: int):
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
