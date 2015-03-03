from flask import g
from flask.ext.restful import abort
from flask.ext.login import current_user

from app.models import User
from app.server import app, db, lm


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
        g.user.id = None
        g.user.admin = app.config["TESTING"]
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

