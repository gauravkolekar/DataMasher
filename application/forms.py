from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from application.models.user import User


class UserRegistrationForm(FlaskForm):
    user_firstname = StringField(label='First Name', validators=[DataRequired()])
    user_lastname = StringField(label='Last Name', validators=[DataRequired()])
    user_email = StringField(label='Email Address', validators=[DataRequired(), Email()])
    user_password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_user_password = PasswordField(label='Confirm Password', validators=[DataRequired(),
                                                                                EqualTo('user_password')])
    submit = SubmitField(label='Sign Up')

    def validate_user_email(self, field):
        if User().validate_email(field.data).count():
            raise ValidationError('This email already exist, please enter a new one')
