from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
# Create Form Classes:

# public search forms:
# Search upcoming flights by city and date:
class public_search_city_form(FlaskForm):
    d_city = StringField('City of Departure', validators=[DataRequired()])
    a_city = StringField('City of Arrival',validators=[DataRequired()])
    s_date = StringField('Date From ',validators=[DataRequired()])
    e_date = StringField('to (same as start date to select 1 day)', validators=[DataRequired()])
    submit = SubmitField('Search')
# Search flights by flight num and date:
class public_search_num_form(FlaskForm): 
    f_num = IntegerField('Flight number (not required)',validators=[DataRequired()])
    s_date = StringField('Departs at Date From ',validators=[DataRequired()])
    e_date = StringField('to (same as start date to select 1 day)',validators=[DataRequired()])
    submit = SubmitField('Search')


# register forms
class customer_register_form(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    name = StringField('Name: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired()])
    building_num = StringField('b_num ', validators=[DataRequired()])
    street = StringField('street ', validators=[DataRequired()])
    city = StringField('city ', validators=[DataRequired()])
    state = StringField('state ', validators=[DataRequired()])
    phone_num = IntegerField('phone  ', validators=[DataRequired()])
    passport_num = StringField('pass_num ', validators=[DataRequired()])
    passport_exp = StringField('pass_exp ', validators=[DataRequired()])
    passport_country = StringField('pass_country ', validators=[DataRequired()])
    birth = StringField('Date of Birth ', validators=[DataRequired()])
    submit = SubmitField('Register')

class staff_register_form(FlaskForm):
    user_name = StringField('u_name', validators=[DataRequired()])
    first_name = StringField('f_name ', validators=[DataRequired()])
    last_name = StringField('l_name ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired()])
    airline_name = StringField('a_name', validators=[DataRequired()])
    birth = StringField('Date of Birth ', validators=[DataRequired()])
    submit = SubmitField('Register')

class booking_agent_register_form(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired()])
    submit = SubmitField('Register')


# Login forms:
class customer_login_form(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')


class staff_login_form(FlaskForm):
    user_name = StringField('u_name', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')


class booking_agent_login_form(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Login')

# User Use forms;

# Customer use filter form:
class user_filter_my_flight_form(FlaskForm):
    d_port = StringField('airport of Departure', validators=[DataRequired()])
    a_port = StringField('airport of Arrival',validators=[DataRequired()])
    date = StringField('Date From ',validators=[DataRequired()])
    submit = SubmitField('Apply Filter')

# Customer use search form:
class customer_search_city_form(FlaskForm):
    d_city = StringField('City of Departure', validators=[DataRequired()])
    a_city = StringField('City of Arrival',validators=[DataRequired()])
    s_date = StringField('Date From ',validators=[DataRequired()])
    e_date = StringField('to (same as start date to select 1 day)', validators=[DataRequired()])
    submit = SubmitField('Search')

# Customer use purchase form:
class customer_purchase_form(FlaskForm):
    num_of_ticket = IntegerField('num of teckets to buy', validators=[DataRequired()])
    submit = SubmitField('Buy Now')

# Customer spend track form: 
class customer_spend_track_form(FlaskForm):
    s_date = StringField('Date From ',validators=[DataRequired()])
    e_date = StringField('to (same as start date to select 1 day)', validators=[DataRequired()])
    submit = SubmitField('Search')


# Booking agent purhches form
class booking_agent_purchase_form(FlaskForm):
    customer_email = StringField('customer email ',validators=[DataRequired()])
    num_of_ticket = IntegerField('num of teckets to buy', validators=[DataRequired()])
    submit = SubmitField('Buy Now')

class change_status_form(FlaskForm):
    status = StringField('status ',validators=[DataRequired()])
    submit = SubmitField('Apply change')


class add_flight_form(FlaskForm):
    flight_num = IntegerField('flight_num',validators=[DataRequired()])
    d_port = StringField('d_port ',validators=[DataRequired()])
    d_time = StringField('d_time', validators=[DataRequired()])
    a_port = StringField('a_port ',validators=[DataRequired()])
    a_time = StringField('a_time', validators=[DataRequired()])
    price = IntegerField('price',validators=[DataRequired()])
    status = StringField('status ',validators=[DataRequired()])
    plane_id = IntegerField('price',validators=[DataRequired()])
    ticket_num = IntegerField('ticket_num',validators=[DataRequired()])
    submit = SubmitField('Add the Flight')


class add_plane_form(FlaskForm):
    plane_id = IntegerField('price',validators=[DataRequired()])
    seat = IntegerField('seat_num',validators=[DataRequired()])
    submit = SubmitField('Add the Airplane')\


class add_port_form(FlaskForm):
    port_name = StringField('d_port ',validators=[DataRequired()])
    city = StringField('d_port ',validators=[DataRequired()])
    submit = SubmitField('Add the Airport')

class add_ba_form(FlaskForm):
    email = StringField('d_port ',validators=[DataRequired()])
    submit = SubmitField('Add the Booking Agent')

class grant_permission_form(FlaskForm):
    user_name = StringField('d_port ',validators=[DataRequired()])
    p_type = StringField('d_port ',validators=[DataRequired()])
    submit = SubmitField('Grant the permission')
