from flask.ext import restful
from flask.ext.restful import abort

from app.forms import UserCreateForm
from app.models import User
from app.serializers import UserSerializer
from app.server import app, db, config, api


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    abort(500)


class UserListView(restful.Resource):
    def get(self):  # list_users
        users = User.query.all()
        return UserSerializer(users, many=True).data

    def post(self):  # create_user
        form = UserCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User(form.username.data, form.password.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data


class UserView(restful.Resource):
    def get(self, id: int):  # get_user
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        return UserSerializer(user).data

    def put(self, id: int):  # change_user
        form = UserCreateForm()
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

    def delete(self, id: int):  # delete_user
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()
        return


api.add_resource(UserListView, '/%s/api/users' % config.App.NAME, endpoint='users')
api.add_resource(UserView, '/%s/api/users/<int:id>' % config.App.NAME, endpoint='user')
