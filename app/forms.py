from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, EqualTo
from app.models import User


class LoginForm(Form):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.found_user = None

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(name=self.name.data).first()
        if user is None:
            self.name.errors.append('User not found')
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Incorrect password')
            return False
        self.found_user = user
        return True


class EditUserForm(Form):
    user_id = HiddenField('user_id')
    name = StringField('name', validators=[DataRequired()])
    is_admin = BooleanField('is_admin')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_name = self.name

    def validate(self):
        if not Form.validate(self):
            return False

        if self.name.data != self.original_name:
            #check if new name is busy
            user = User.query.filter(
                User.name == self.name.data,
                User.id != self.user_id.data
            ).first()
            if user is not None:
                self.name.errors.append('Name is busy.')
                return False
        return True


class NewUserForm(Form):
    name = StringField('name', validators=[DataRequired()])
    is_admin = BooleanField('is_admin')
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[EqualTo('password')])

    def validate(self):
        if not Form.validate(self):
            return False

        #check if new name is busy
        user = User.query.filter(
            User.name == self.name.data,
        ).first()
        if user is not None:
            self.name.errors.append('Name is busy.')
            return False

        return True


class NewPasswordForm(Form):
    user_id = HiddenField('user_id')
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[EqualTo('password')])
