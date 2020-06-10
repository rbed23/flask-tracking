# flask_tracking/users/forms.py
from flask_wtf import Form
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError

from .models import User


class LoginForm(Form):
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.StringField(validators=[InputRequired()])

    # WTForms supports "inline" validators
    # which are methods of our `Form` subclass
    # with names in the form `validate_[fieldname]`.
    # This validator will run after all the
    # other validators have passed.
    def validate_password(self, field=None):
        try:
            user = User.query.filter(User.email == self.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user: none found")
        if user is None:
            raise ValidationError("Invalid user: none")
        if not user.is_valid_password(self.password.data):
            raise ValidationError("Invalid password")


        # Make the current user available
        # to calling code.
        self.user = user


class RegistrationForm(Form):
    name = fields.StringField("Display Name")
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.StringField(validators=[InputRequired()])

    def validate_email(form, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists")
