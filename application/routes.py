from flask import render_template, request, make_response, jsonify, abort
from application import app
from application.forms import UserRegistrationForm
from application.models.user import User
from application.models.yelp_data import YelpData


@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    user_registration_form = UserRegistrationForm()
    if user_registration_form.validate_on_submit():
        client_key = User().add_user(firstname=user_registration_form.user_firstname.data,
                        lastname=user_registration_form.user_lastname.data,
                        email=user_registration_form.user_email.data,
                        password=user_registration_form.user_password.data)
        return render_template('api_key_h.html', api_key=client_key)
    return render_template('register_h.html', form=user_registration_form)


@app.route('/api/v1.0/yelp_business_match', methods=['POST'])
def yelp_business_match():
    if 'Authorization' not in request.headers:
        abort(401)

    if not User().verify_key(request.headers.get('Authorization')):
        abort(401)

    if not request.is_json:
        abort(400)

    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400)

    if 'name' not in request_data or 'street_address' not in request_data or 'city' not in request_data \
            or 'state' not in request_data or 'country' not in request_data:
        return make_response(jsonify({'error': 'Missing required attributes'}), 400)

    user_id = User().get_user_id(request.headers.get('Authorization'))

    YelpData().yelp_request(yelp_request=request_data, user_id=user_id)

    data = YelpData().get_business_match_data(user_id=user_id,
                                       name=request_data['name'],
                                       address1=request_data['street_address'],
                                       city=request_data['city'],
                                       state=request_data['state'],
                                       country=request_data['country'])

    return jsonify(data)


@app.route('/api/v1.0/yelp_business_details/<yelp_id>', methods=['GET'])
def yelp_business_details(yelp_id):
    pass


@app.route('/api/v1.0/yelp_business_reviews/<yelp_id>', methods=['GET'])
def yelp_business_reviews(yelp_id):
    pass


@app.route('/api/v1.0/yelp_aggregates', methods=['GET'])
def yelp_business_aggregates():
    pass


@app.errorhandler(401)
def authorization_error():
    return make_response(jsonify({'error': 'Authorization error'}), 401)


@app.errorhandler(400)
def bad_request_error():
    return make_response(jsonify({'error': 'Bad Request'}), 400)



