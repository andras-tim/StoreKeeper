from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_alchemy import model_form_factory

from app.server import db
from app.models import User


BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        return db.session


class UserCreateForm(ModelForm):
    class Meta(object):
        model = User


class SessionCreateForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
