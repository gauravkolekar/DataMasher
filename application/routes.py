from flask import render_template, redirect, url_for
from application import app
from application.forms import UserRegistration
from application.models import User


@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    user_registration_form = UserRegistration()
    if user_registration_form.validate_on_submit():
        print('First Name: {} \n Last Name: {} \n Email: {} \n Password: {}'.format(user_registration_form.user_firstname.data,
                                                                                    user_registration_form.user_lastname.data,
                                                                                    user_registration_form.user_email.data,
                                                                                    user_registration_form.user_password.data))
        user = User()
        user.add_user(firstname=user_registration_form.user_firstname.data,
                      lastname=user_registration_form.user_lastname.data,
                      email=user_registration_form.user_email.data,
                      password=user_registration_form.user_password.data)
        return redirect(url_for('index'))
    return render_template('register_h.html', form=user_registration_form)
