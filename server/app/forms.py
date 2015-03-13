from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_alchemy import model_form_factory

from app.server import db
from app.models import User, Vendor, Unit


BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        return db.session


class UserCreateForm(ModelForm):
    class Meta(object):
        model = User
        exclude = ["password_hash"]
    password = StringField('password', validators=[DataRequired()])


class UserUpdateForm(ModelForm):
    class Meta(object):
        model = User
        exclude = ["password_hash"]
        all_fields_optional = True
        assign_required = False
    password = StringField('password')


class VendorCreateForm(ModelForm):
    class Meta(object):
        model = Vendor


class VendorUpdateForm(ModelForm):
    class Meta(object):
        model = Vendor
        all_fields_optional = True
        assign_required = False


class UnitCreateForm(ModelForm):
    class Meta(object):
        model = Unit


class UnitUpdateForm(ModelForm):
    class Meta(object):
        model = Unit
        all_fields_optional = True
        assign_required = False


class SessionCreateForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
