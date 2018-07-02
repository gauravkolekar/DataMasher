from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class UserRegistration(FlaskForm):
    user_firstname = StringField(label='First Name', validators=[DataRequired()])
    user_lastname = StringField(label='Last Name', validators=[DataRequired()])
    user_email = StringField(label='Email Address', validators=[DataRequired(), Email(message='Email Address Required')])
    user_password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_user_password = PasswordField(label='Confirm Password', validators=[DataRequired(),
                                                                                EqualTo('user_password',
                                                                                        message='Password should match')])
    submit = SubmitField(label='Sign Up')
