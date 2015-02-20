from flask import g
from flask.ext import restful
from flask.ext.restful import abort
from flask.ext.login import login_user, logout_user, current_user, login_required

from app.forms import UserCreateForm, SessionCreateForm
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

    @login_required
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

    @login_required
    def delete(self, id: int):  # delete_user
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()
        return


class SessionView(restful.Resource):
    def get(self):  # check is logged in
        if not g.user.is_authenticated():
            abort(401)
        user = User.get_user(g.user.username)
        return UserSerializer(user).data

    def post(self):  # login
        form = SessionCreateForm()
        if not form.validate_on_submit():
            abort(422, message=form.errors)

        user = User.get_user(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return UserSerializer(user).data, 201
        abort(401)

    @login_required
    def delete(self):  # logout
        logout_user()
        return

api.add_resource(UserListView, '/%s/api/users' % config.App.NAME, endpoint='users')
api.add_resource(UserView, '/%s/api/users/<int:id>' % config.App.NAME, endpoint='user')
api.add_resource(SessionView, '/%s/api/sessions' % config.App.NAME, endpoint='sessions')
