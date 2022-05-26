# database project
# author: Jax Li & Cassie Huang

#Import Library
from flask import Flask, render_template, flash, request, session, url_for, redirect
import pymysql.cursors
import random
from datetime import datetime
from form_class import public_search_city_form, public_search_num_form, customer_register_form ,\
                    booking_agent_register_form, staff_register_form, customer_login_form, \
                    staff_login_form, booking_agent_login_form, user_filter_my_flight_form, \
                    customer_search_city_form,customer_purchase_form, customer_spend_track_form,\
                    booking_agent_purchase_form,change_status_form,add_flight_form, add_plane_form,\
                    add_port_form, add_ba_form, grant_permission_form
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
conn = pymysql.connect(host='localhost',
                       user='root',
                       port = 3306,
                       passwd='12345678',
                       db='db_project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Create flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key nobody knows'

# Create Form Classes:
# Sample Form: 
# class NamerForm(FlaskForm):
#     name = StringField('City of Departure', validators=[DataRequired()])
#     submit = SubmitField('Search')

# Sample.route
# @app.route('/name', methods = ['GET', 'POST'])
# def name():
#     name = None
#     form = NamerForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#     return render_template('name.html', name = name, form = form)


# frount page 
@app.route('/')
def index():
    return render_template('index.html')

#--------------------------------------------------- handeling errors----------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500



#---------------------------------------------------Public Search----------------------------------------------------------------



# public search by city page
@app.route('/public_search_city', methods = ['GET', 'POST'])
def public_search_city():
    d_city = None
    a_city = None
    s_date = None
    e_date = None
    form = public_search_city_form()
    data_got = None
    cursor = conn.cursor()
    if form.validate_on_submit():
        d_city = form.d_city.data
        a_city = form.a_city.data
        s_date = form.s_date.data
        e_date = form.e_date.data
        if s_date == 'all':
            query = "SELECT * FROM flight, airport as ad, airport as aa \
                        WHERE flight.departure_airport = ad.airport_name and \
                        flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                        ad.airport_city = %s and aa.airport_city = %s order by departure_time"
            cursor.execute(query, (d_city, a_city))
        elif s_date == e_date:
            query = "SELECT * FROM flight, airport as ad, airport as aa \
                        WHERE flight.departure_airport = ad.airport_name and \
                        flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                        ad.airport_city = %s and aa.airport_city = %s and \
                        convert(departure_time,date) = %s order by departure_time"
            cursor.execute(query, (d_city, a_city, s_date))
        else:
            query = "SELECT * FROM flight, airport as ad, airport as aa \
                        WHERE flight.departure_airport = ad.airport_name and \
                        flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                        ad.airport_city = %s and aa.airport_city = %s and \
                        convert(departure_time,date) between %s and %s order by departure_time"
            cursor.execute(query, (d_city, a_city, s_date, e_date))

    else:
        query = "SELECT * FROM flight, airport as ad, airport as aa \
        WHERE flight.departure_airport = ad.airport_name and \
            flight.arrival_airport = aa.airport_name \
            order by departure_time"
        cursor.execute(query)
    data_got = cursor.fetchall()
    cursor.close()

    return render_template('public_search_city.html', 
                d_city = d_city,
                a_city = a_city,
                s_date = s_date,
                e_date = e_date,
                form = form, 
                data_got = data_got)

# public search by flioght number page
@app.route('/public_search_num', methods = ['GET', 'POST'])
def public_search_num():
    f_num = None
    s_date = None
    e_date = None
    form = public_search_num_form()
    data_got = None
    cursor = conn.cursor()
    if form.validate_on_submit():
        f_num = form.f_num.data
        s_date = form.s_date.data
        e_date = form.e_date.data
        if s_date == 'all':
            query = "SELECT * FROM flight WHERE flight_num = %s order by departure_time"
            cursor.execute(query, (f_num))
        elif s_date == e_date:
            query = "SELECT * FROM flight WHERE flight_num = %s and \
                    convert(departure_time,date) = %s order by departure_time"
            cursor.execute(query, (f_num, s_date))
        else:
            query = "SELECT * FROM flight WHERE flight_num = %s and \
                    convert(departure_time,date) between %s and %s order by departure_time"
            cursor.execute(query, (f_num, s_date, e_date))

    else:
        query = "SELECT * FROM flight \
            order by departure_time"
        cursor.execute(query)
    data_got = cursor.fetchall()
    cursor.close()

    return render_template('public_search_num.html', 
                f_num = f_num,
                s_date = s_date,
                e_date = e_date,
                form = form,
                data_got = data_got)




#---------------------------------------------------Register----------------------------------------------------------------

# Customer register:
@app.route('/register_customer', methods = ['GET', 'POST'])
def register_customer():
    email = None
    name = None
    password = None
    c_password = None
    building_num = None
    street = None
    city = None
    state = None
    phone_num = None
    passport_num = None
    passport_exp = None
    passport_country = None
    birth = None
    form  = customer_register_form()
    cursor = conn.cursor()
    if form.validate_on_submit():
            email = form.email.data
            name = form.name.data
            password = form.password.data
            c_password = form.confirm_password.data
            building_num = form.building_num.data
            street = form.street.data
            city = form.city.data
            state = form.state.data
            phone_num = form.phone_num.data
            passport_num = form.passport_num.data
            passport_exp = form.passport_exp.data
            passport_country = form.passport_country.data
            birth = form.birth.data
            query_to_get_exist_email = 'SELECT email FROM customer WHERE email = %s'
            cursor.execute(query_to_get_exist_email, (email))
            check_email = cursor.fetchall()
            if len(check_email) == 0:
                insert_query = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(insert_query, (email, name, password, building_num, street, city, state, phone_num, passport_num, passport_exp, passport_country, birth))    
                conn.commit()
            else:
                email = 'exist'
    cursor.close()
    return render_template('register_customer.html', 
                email = email,
                name = name,
                password = password,
                c_password = c_password,
                building_num = building_num,
                street = street,
                city = city,
                state = state, 
                phone_num = phone_num,
                passport_num = passport_num,
                passport_exp = passport_exp,
                passport_country = passport_country, 
                birth = birth,
                form = form)

# Airline staff register form :
@app.route('/register_staff', methods = ['GET', 'POST'])
def register_staff():
    airline_name = None
    user_name = None
    first_name = None
    last_name = None
    password = None
    c_password = None
    birth = None
    form  = staff_register_form()
    cursor = conn.cursor()
    if form.validate_on_submit():
            airline_name = form.airline_name.data
            user_name = form.user_name.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data
            birth = form.birth.data
            c_password = form.confirm_password.data
            query_to_get_exist_user = 'SELECT username FROM airline_staff WHERE username = %s'
            cursor.execute(query_to_get_exist_user, (user_name))
            check_user = cursor.fetchall()
            if len(check_user) == 0:
                insert_query = 'INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s, %s)' 
                cursor.execute(insert_query, (user_name, password, first_name, last_name, birth, airline_name))
                conn.commit()
            else:
                user_name = 'exist'
    cursor.close()
    return render_template('register_staff.html', 
                airline_name = airline_name,
                user_name = user_name,
                first_name = first_name,
                last_name = last_name,
                password = password,
                c_password = c_password,
                birth = birth,
                form = form)

# Booking agent register form :
@app.route('/register_booking_agent', methods = ['GET', 'POST'])
def register_booking_agent():
    email = None
    password = None
    form  = booking_agent_register_form()
    ba_id = None
    c_password = None
    cursor = conn.cursor()
    if form.validate_on_submit():
        query_to_get_exist_email = 'SELECT email FROM booking_agent WHERE email = %s'
        cursor.execute(query_to_get_exist_email, (form.email.data))
        check_email = cursor.fetchall()
        email = form.email.data
        password = form.password.data
        c_password = form.confirm_password.data
        if len(check_email) == 0:
            ba_id = random.randint(1,9999)
            query_to_set_id = 'SELECT MAX(booking_agent_id) FROM booking_agent'
            cursor.execute(query_to_set_id)
            ba_id = list(cursor.fetchall()[0].values())[0] + 1
            # insert the ba to the database
            insert_query = 'INSERT INTO booking_agent VALUES(%s, md5(%s), %s)' 
            cursor.execute(insert_query, (email, password, ba_id))
            conn.commit()
        else: 
            email = 'exist'
    cursor.close()
    return render_template('register_booking_agent.html', 
                email = email,
                password = password,
                c_password = c_password,
                ba_id = ba_id,
                form = form)



#---------------------------------------------------Login & Logout----------------------------------------------------------------

# Customer Login Form:
@app.route('/login_customer', methods = ['GET', 'POST'])
def login_customer():
    email = None
    password = None
    form  = customer_login_form()
    cursor = conn.cursor()
    if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            query_to_get_exist_user = 'SELECT email, password, name FROM customer WHERE email = %s AND password = md5(%s)'
            cursor.execute(query_to_get_exist_user, (email, password))
            check = cursor.fetchall()
            cursor.close()
            if len(check) == 0:
                email = None
                password = None
                flash('Account and password do not match, please try again')
            else:
                session['user_id'] = email
                # session['user_name'] = name
                name = list(check[0].values())[2]
                form = user_filter_my_flight_form()
                return redirect(url_for('customer_home'))
    return render_template('login_customer.html', 
                email = email,
                password = password,
                form = form)

# Staff Login Form:
@app.route('/login_staff', methods = ['GET', 'POST'])
def login_staff():
    username = None
    password = None
    form  = staff_login_form()
    cursor = conn.cursor()
    if form.validate_on_submit():
            username = form.user_name.data
            password = form.password.data
            query_to_get_exist_user = 'SELECT username, password, first_name FROM airline_staff WHERE username = %s AND password = md5(%s)'
            cursor.execute(query_to_get_exist_user, (username, password))
            check = cursor.fetchall()
            cursor.close()
            if len(check) == 0:
                username = None
                password = None
                flash('Account and password do not match, please try again')
            else:
                session['user_id'] = username
                name = list(check[0].values())[2]
                return redirect(url_for('staff_home'))
    return render_template('login_staff.html', 
                user_name = username,
                password = password,
                form = form)

# Booking agent Login Form:
@app.route('/login_booking_agent', methods = ['GET', 'POST'])
def login_booking_agent():
    email = None
    password = None
    form  = booking_agent_login_form()
    cursor = conn.cursor()
    if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            query_to_get_exist_user = 'SELECT email, password FROM booking_agent WHERE email = %s AND password = md5(%s)'
            cursor.execute(query_to_get_exist_user, (email, password))
            check = cursor.fetchall()
            cursor.close()
            if len(check) == 0:
                email  = None
                password = None
                flash('Account and password do not match, please try again')
            else:
                session['user_id'] = email
                name = email
                return redirect(url_for('booking_agent_home'))

    return render_template('login_booking_agent.html', 
                email = email,
                password = password,
                form = form)


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('user_id')
    flash('You are logged out.')
    return render_template('index.html')

#---------------------------------------------------Cuastomer Use----------------------------------------------------------------

# Customer home page
@app.route('/home_customer', methods = ['GET', 'POST'])
def customer_home():
    form = user_filter_my_flight_form()
    user_id = session['user_id']
    defalt = True
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))

    if user_id == session['user_id']:
        date = None
        d_port = None
        a_port = None
        defalt = True
        if form.validate_on_submit():
            d_port = form.d_port.data
            a_port = form.a_port.data
            date = form.date.data
            cursor = conn.cursor()
            if date == 'all':
                if d_port == 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s \
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id))
                elif d_port == 'all' and a_port != 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and f.arrival_airport = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, a_port))
                elif d_port != 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and f.departure_airport = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, d_port))
                else:
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and f.departure_airport = %s and f.arrival_airport = %s \
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, d_port, a_port))
            else:
                if d_port == 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, date))
                elif d_port == 'all' and a_port != 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and f.arrival_airport = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, a_port, date))
                elif d_port != 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and f.departure_airport = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, d_port, date))
                else:
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.customer_email = %s and f.departure_airport = %s and f.arrival_airport = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (user_id, d_port, a_port, date))
            defalt = False
            data_got = cursor.fetchall()
            cursor.close()
            flash('Filter applied successfilly !')
        else:
            cursor = conn.cursor()
            query = "SELECT DISTINCT f.*\
                        FROM ticket as t \
                        join flight as f on t.flight_num = f.flight_num\
                        join purchases as p on t.ticket_id = p.ticket_id\
                        where p.customer_email = %s \
                        and f.status = 'upcoming'"
            cursor.execute(query, (user_id))
            data_got = cursor.fetchall()
            cursor.close()


        return render_template('home_customer.html', 
                                    user_id = user_id, 
                                    data_got = data_got,
                                    defalt = defalt,
                                    form = form)

    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

# Customer search 
@app.route('/search_customer', methods = ['GET', 'POST'])
def customer_search():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        d_city = None
        a_city = None
        s_date = None
        e_date = None
        form = customer_search_city_form()
        data_got = None
        cursor = conn.cursor()
        if form.validate_on_submit():
            d_city = form.d_city.data
            a_city = form.a_city.data
            s_date = form.s_date.data
            e_date = form.e_date.data
            if s_date == 'all':
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                            ad.airport_city = %s and aa.airport_city = %s order by departure_time"
                cursor.execute(query, (d_city, a_city))
            elif s_date == e_date:
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                            ad.airport_city = %s and aa.airport_city = %s and \
                            convert(departure_time,date) = %s order by departure_time"
                cursor.execute(query, (d_city, a_city, s_date))
            else:
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                            ad.airport_city = %s and aa.airport_city = %s and \
                            convert(departure_time,date) between %s and %s order by departure_time"
                cursor.execute(query, (d_city, a_city, s_date, e_date))

        else:
            query = "SELECT * FROM flight, airport as ad, airport as aa \
            WHERE flight.departure_airport = ad.airport_name and \
                flight.arrival_airport = aa.airport_name \
                order by departure_time"
            cursor.execute(query)
        data_got = cursor.fetchall()
        cursor.close()

        return render_template('customer_search_city.html', 
                    d_city = d_city,
                    a_city = a_city,
                    s_date = s_date,
                    e_date = e_date,
                    form = form, 
                    data_got = data_got, 
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

# Customer purchase
@app.route('/purchase_customer/<int:flight_num>', methods = ['GET', 'POST'])
def customer_purchase(flight_num):
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        form = customer_purchase_form()
        # try: 
        cursor = conn.cursor()
        query = 'SELECT ticket_id from ticket where flight_num = %s and \
        ticket_id not in (SELECT ticket_id from purchases)'
        cursor.execute(query, (flight_num))
        data_got = cursor.fetchall()
        cursor.close()
        if data_got:
            ticket_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
        else:
            ticket_lis = []
        ticket_count = len(ticket_lis)
        if ticket_count == 0:
            return render_template('customer_purchase.html',
                flight_num = flight_num,
                ticket_count = ticket_count, 
                form = form)
        else:
            # form = customer_purchase_form()
            num_of_ticket = None
            if form.validate_on_submit():
                num_of_tecket = form.num_of_ticket.data
                if num_of_tecket > ticket_count:
                        flash('Error: not enough tickets left')
                        return render_template('customer_purchase.html',
                                flight_num = flight_num,
                                ticket_count = ticket_count,
                                num_of_ticket = num_of_ticket,
                                form = form)
                else:
                    cursor = conn.cursor()
                    for i in range(num_of_tecket):
                        purchase_date = datetime.now().strftime("%Y-%m-%d")
                        query = "insert into purchases values (%s, %s, null, %s);"
                        cursor.execute(query, (ticket_lis.pop(), user_id, purchase_date))
                        conn.commit()
                    flash('Ticket(s) purchased successfully !')
                    return render_template('customer_purchase.html',
                                flight_num = flight_num,
                                ticket_count  = ticket_count,
                                num_of_ticket = num_of_ticket,
                                form = form)
            else:
                    return render_template('customer_purchase.html',
                                flight_num = flight_num,
                                ticket_count  = ticket_count,
                                num_of_ticket = num_of_ticket,
                                form = form)

        # except:
        #     flash('Error')
        #     return render_template('purchase.html',
        #                             form = None)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

# Customer track the spand
@app.route('/spend_track', methods = ['GET', 'POST'])
def spend_track():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        form = customer_spend_track_form()
        s_date = None
        e_date = None
        data_got_totol = None
        data_got_month = None
        defalt = True
        cursor = conn.cursor()
        if form.validate_on_submit():
            s_date = form.s_date.data
            e_date = form.e_date.data
            defalt = False
            if s_date == 'all' and e_date == 'all':
                query_month = "select month(purchase_date) as month, sum(price) as money\
                from flight join ticket using(airline_name, flight_num) join purchases using(ticket_id)\
                where customer_email = %s \
                group by month(purchase_date);"
                cursor.execute(query_month, (user_id))
                data_got_month = cursor.fetchall()

                query_total = "select sum(price) as money\
                from flight join ticket using(airline_name, flight_num) join purchases using(ticket_id)\
                where customer_email = %s ;"
                cursor.execute(query_total, (user_id))
                data_got_totol = cursor.fetchone()
            else:
                query_total = "select sum(price) as money\
                from flight join ticket using(airline_name, flight_num) join purchases using(ticket_id)\
                where customer_email = %s and purchase_date between %s and %s"
                cursor.execute(query_total, (user_id, s_date, e_date))
                data_got_totol = cursor.fetchone()

                query_month = "select month(purchase_date) as month, sum(price) as money\
                from flight join ticket using(airline_name, flight_num) join purchases using(ticket_id)\
                where customer_email = %s and purchase_date between %s and %s group by month(purchase_date);"
                cursor.execute(query_month, (user_id, s_date, e_date))
                data_got_month = cursor.fetchone()
            return render_template("spand_track.html", 
                        data_got_month = data_got_month, 
                        data_got_totol = data_got_totol, 
                        s_date = s_date,
                        e_date = e_date,
                        form = form,
                        defalt = defalt)


        else:
            query_month = "select month(purchase_date) as month, sum(price) as money\
                from flight join ticket using(airline_name, flight_num) join purchases using(ticket_id)\
                where customer_email = %s and date_sub(curdate(), interval 6 month)<= purchase_date\
                group by month(purchase_date);"
            cursor.execute(query_month, (user_id))
            data_got_month = cursor.fetchall()
            query_total = "select sum(price) as money\
                from flight join ticket using(airline_name, flight_num) join purchases using(ticket_id)\
                where customer_email = %s and date_sub(curdate(), interval 1 year)<= purchase_date;"
            cursor.execute(query_total, (user_id))
            data_got_totol = cursor.fetchone()
            return render_template("spand_track.html", 
                                    data_got_month = data_got_month, 
                                    data_got_totol = data_got_totol, 
                                    s_date = s_date,
                                    e_date = e_date,
                                    form = form,
                                    defalt = defalt)


    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))





#---------------------------------------------------Booking Agent Use----------------------------------------------------------------

# Booking Agent Homepage
@app.route('/home_booking_agent', methods = ['GET', 'POST'])
def booking_agent_home():
    form = user_filter_my_flight_form()
    user_id = session['user_id']
    defalt = True
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))

    if user_id == session['user_id']:
        date = None
        d_port = None
        a_port = None
        defalt = True
        cursor = conn.cursor()
        # get my booking agent id:
        query = "SELECT booking_agent_id from booking_agent where email = %s"
        cursor.execute(query, (user_id))
        ba_id  = list(cursor.fetchall()[0].values())[0]

        if form.validate_on_submit():
            d_port = form.d_port.data
            a_port = form.a_port.data
            date = form.date.data

            if date == 'all':
                if d_port == 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s \
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id))
                elif d_port == 'all' and a_port != 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and f.arrival_airport = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, a_port))
                elif d_port != 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and f.departure_airport = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, d_port))
                else:
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and f.departure_airport = %s and f.arrival_airport = %s \
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, d_port, a_port))
            else:
                if d_port == 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, date))
                elif d_port == 'all' and a_port != 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and f.arrival_airport = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, a_port, date))
                elif d_port != 'all' and a_port == 'all':
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and f.departure_airport = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, d_port, date))
                else:
                    query = "SELECT DISTINCT f.*\
                            FROM ticket as t \
                            join flight as f on t.flight_num = f.flight_num\
                            join purchases as p on t.ticket_id = p.ticket_id\
                            where p.booking_agent_id = %s and f.departure_airport = %s and f.arrival_airport = %s and convert(departure_time,date) = %s\
                            and f.status = 'upcoming'"
                    cursor.execute(query, (ba_id, d_port, a_port, date))
            defalt = False
            data_got = cursor.fetchall()
            cursor.close()
            flash('Filter applied successfilly !')
        else:
            cursor = conn.cursor()
            query = "SELECT DISTINCT f.*\
                        FROM ticket as t \
                        join flight as f on t.flight_num = f.flight_num\
                        join purchases as p on t.ticket_id = p.ticket_id\
                        where p.booking_agent_id = %s \
                        and f.status = 'upcoming'"
            cursor.execute(query, (ba_id))
            data_got = cursor.fetchall()
            cursor.close()


        return render_template('home_booking_agent.html', 
                                    user_id = user_id, 
                                    data_got = data_got,
                                    defalt = defalt,
                                    form = form)

    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

# Booking Agent Search
@app.route('/search_booking_agent', methods = ['GET', 'POST'])
def booking_agent_search():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        d_city = None
        a_city = None
        s_date = None
        e_date = None
        form = customer_search_city_form()
        data_got = None
        cursor = conn.cursor()
        
        if form.validate_on_submit():
            d_city = form.d_city.data
            a_city = form.a_city.data
            s_date = form.s_date.data
            e_date = form.e_date.data
            if s_date == 'all':
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                            ad.airport_city = %s and aa.airport_city = %s and flight.airline_name in (select airline_name from booking_agent_work_for where email = %s) \
                            order by departure_time"
                cursor.execute(query, (d_city, a_city,user_id))
            elif s_date == e_date:
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                            ad.airport_city = %s and aa.airport_city = %s and \
                            convert(departure_time,date) = %s and flight.airline_name in (select airline_name from booking_agent_work_for where email = %s) order by departure_time"
                cursor.execute(query, (d_city, a_city, s_date, user_id))
            else:
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and flight.status = 'Upcoming' and\
                            ad.airport_city = %s and aa.airport_city = %s and flight.airline_name in (select airline_name from booking_agent_work_for where email = %s) and \
                            convert(departure_time,date) between %s and %s order by departure_time"
                cursor.execute(query, (d_city, a_city,user_id, s_date, e_date))

        else:
            query = "SELECT * FROM flight, airport as ad, airport as aa \
                WHERE flight.departure_airport = ad.airport_name and \
                flight.arrival_airport = aa.airport_name and flight.airline_name in (select airline_name from booking_agent_work_for where email = %s)\
                order by departure_time"
            cursor.execute(query, (user_id))
        data_got = cursor.fetchall()
        cursor.close()

        return render_template('booking_agent_search_city.html', 
                    d_city = d_city,
                    a_city = a_city,
                    s_date = s_date,
                    e_date = e_date,
                    form = form, 
                    data_got = data_got, 
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

# Booking Agent Purchase
@app.route('/purchase_booking_agent/<int:flight_num>', methods = ['GET', 'POST'])
def booking_agent_purchase(flight_num):
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        form = booking_agent_purchase_form()
        # try: 
        # Get the available ticket id
        cursor = conn.cursor()
        query = 'SELECT ticket_id from ticket where flight_num = %s and \
        ticket_id not in (SELECT ticket_id from purchases)'
        cursor.execute(query, (flight_num))
        data_got = cursor.fetchall()
        if data_got:
            ticket_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
        else:
            ticket_lis = []
        ticket_count = len(ticket_lis)

        # get the ba_id
        query = "SELECT booking_agent_id from booking_agent where email = %s"
        cursor.execute(query, (user_id))
        ba_id  = list(cursor.fetchall()[0].values())[0]


        if ticket_count == 0:
            return render_template('booking_agent_purchase.html',
                flight_num = flight_num,
                ticket_count = ticket_count, 
                form = form)
        else:
            # form = customer_purchase_form()
            num_of_ticket = None
            customer_email = None
            if form.validate_on_submit():
                num_of_tecket = form.num_of_ticket.data
                customer_email = form.customer_email.data
                if num_of_tecket > ticket_count:
                        flash('Error: not enough tickets left')
                        return render_template('booking_agent_purchase.html',
                                flight_num = flight_num,
                                ticket_count = ticket_count,
                                num_of_ticket = num_of_ticket,
                                customer_email = customer_email ,
                                form = form)
                else:
                    cursor = conn.cursor()
                    for i in range(num_of_tecket):
                        purchase_date = datetime.now().strftime("%Y-%m-%d")
                        query = "insert into purchases values (%s, %s, %s, %s);"
                        cursor.execute(query, (ticket_lis.pop(), customer_email ,ba_id, purchase_date))
                        conn.commit()
                    flash('Ticket(s) purchased successfully !')
                    return render_template('booking_agent_purchase.html',
                                flight_num = flight_num,
                                ticket_count  = ticket_count,
                                customer_email = customer_email ,
                                num_of_ticket = num_of_ticket,
                                form = form)
            else:
                    return render_template('booking_agent_purchase.html',
                                flight_num = flight_num,
                                ticket_count  = ticket_count,
                                num_of_ticket = num_of_ticket,
                                customer_email = customer_email ,
                                form = form)

        # except:
        #     flash('Error')
        #     return render_template('purchase.html',
        #                             form = None)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

# Booking agent view commission
# Customer track the spand
@app.route('/commission_booking_agent', methods = ['GET', 'POST'])
def view_commission():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        form = customer_spend_track_form()
        s_date = None
        e_date = None
        data_got_avg = 0
        data_got_ticket = 0
        data_got_totol = 0
        defalt = True
        cursor = conn.cursor()
        if form.validate_on_submit():
            s_date = form.s_date.data
            e_date = form.e_date.data
            defalt = False
            if s_date == 'all' and e_date == 'all':

                query_total = "Select round(sum(0.1*price),2) as total_commission\
                    From flight join ticket using(flight_num, airline_name) join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
                    Where booking_agent.email = %s "
                cursor.execute(query_total, (user_id))
                data_got_totol = cursor.fetchall()
                query_ticket = "Select count(ticket_id) as ticket_num\
                    From ticket join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
                    Where booking_agent.email = %s "
                cursor.execute(query_ticket, (user_id))
                data_got_ticket = cursor.fetchall() 

            else:
                query_total ="Select round(sum(0.1*price),2) as total_commission\
                    From flight join ticket using(flight_num, airline_name) join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
                    Where booking_agent.email = %s and purchase_date between %s and %s group by month(purchase_date);"
                cursor.execute(query_total, (user_id, s_date, e_date))
                data_got_totol = cursor.fetchall()

                query_ticket = "Select count(ticket_id) as ticket_num\
                    From ticket join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
                    Where booking_agent.email = %s and purchase_date between %s and %s group by month(purchase_date);"
                cursor.execute(query_ticket, (user_id,s_date, e_date))
                data_got_ticket = cursor.fetchall() 
            if list(data_got_ticket[0].values())[0] != 0:
                data_got_avg = list(data_got_totol[0].values())[0] / list(data_got_ticket[0].values())[0]
                data_got_totol = list(data_got_totol[0].values())[0]
                data_got_ticket = list(data_got_ticket[0].values())[0]
            cursor.close()
            return render_template("view_commission.html", 
                        data_got_avg = data_got_avg, 
                        data_got_totol = data_got_totol,                                     
                        data_got_ticket = data_got_ticket,
                        s_date = s_date,
                        e_date = e_date,
                        form = form,
                        defalt = defalt)

        else:
            query_ticket = "Select count(ticket_id) as ticket_num\
                    From ticket join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
                    Where booking_agent.email = %s and date_sub(curdate(), interval 30 day) <= purchase_date;"
            cursor.execute(query_ticket, (user_id))
            data_got_ticket = cursor.fetchall() 

            query_total =  "Select round(sum(0.1*price),2) as total_commission\
                    From flight join ticket using(flight_num, airline_name) join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
                    Where booking_agent.email = %s and date_sub(curdate(), interval 30 day) <= purchase_date;"
            cursor.execute(query_total, (user_id))
            data_got_totol = cursor.fetchall()
            if list(data_got_ticket[0].values())[0] != 0:
                data_got_avg = list(data_got_totol[0].values())[0] / list(data_got_ticket[0].values())[0]
                data_got_totol = list(data_got_totol[0].values())[0]
                data_got_ticket = list(data_got_ticket[0].values())[0]
            cursor.close()
            return render_template("view_commission.html", 
                                    data_got_avg = data_got_avg, 
                                    data_got_totol = data_got_totol, 
                                    data_got_ticket = data_got_ticket,
                                    s_date = s_date,
                                    e_date = e_date,
                                    form = form,
                                    defalt = defalt)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))

@app.route('/top_customer', methods = ['GET', 'POST'])
def top_customer():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
            cursor = conn.cursor()
            # top 5 customers based on # of tickets in 6 months
            query1 = "Select customer_email, count(ticket_id) as count\
            From purchases join booking_agent using(booking_agent_id)\
            Where booking_agent.email = %s and date_sub(curdate(), interval 6 month) <= purchase_date\
            Group by customer_email order by count desc Limit 0, 5;"
            cursor.execute(query1, (user_id))
            data1 = cursor.fetchall()

            query2 = "Select customer_email, sum(0.1*price) as total\
            From ticket join flight using(flight_num, airline_name) join purchases using(ticket_id) join booking_agent using(booking_agent_id)\
            Where booking_agent.email = %s and date_sub(curdate(), interval 1 year) <= purchase_date\
            Group by customer_email order by total desc Limit 0, 5;"
            cursor.execute(query2, (user_id))
            data2 = cursor.fetchall()
            cursor.close()
            return render_template("top_customer.html", 
                                    user_id = user_id, 
                                    data1 = data1, 
                                    data2 = data2)

    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))





#---------------------------------------------------Airline Staff Use----------------------------------------------------------------

# Airline Staff home page
@app.route('/home_staff', methods = ['GET', 'POST'])
def staff_home():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))

    if user_id == session['user_id']:
        cursor = conn.cursor()

        # get the name of the user and the airline name
        name_query = 'select first_name, airline_name from airline_staff where username = %s'
        cursor.execute(name_query ,(user_id))
        name = cursor.fetchall()
        first_name = list(name[0].values())[0]
        line_name = list(name[0].values())[1]
        # get the next 30 flight by the company
        query = "SELECT * FROM flight \
            WHERE airline_name = %s and date_sub(curdate(), interval 1 month)<=departure_time and departure_time >= curdate()\
            order by departure_time"
        cursor.execute(query ,(line_name))
        data_got = cursor.fetchall()
        return render_template('home_staff.html', 
                                    user_id = user_id, 
                                    data_got = data_got,
                                    first_name = first_name, 
                                    line_name = line_name)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# airline staff search flight
@app.route('/search_flight_staff', methods = ['GET', 'POST'])
def staff_search():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        d_city = None
        a_city = None
        s_date = None
        e_date = None
        form = customer_search_city_form()
        data_got = None
        cursor = conn.cursor()
        
        if form.validate_on_submit():
            d_city = form.d_city.data
            a_city = form.a_city.data
            s_date = form.s_date.data
            e_date = form.e_date.data
            if s_date == 'all':
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name and\
                            ad.airport_city = %s and aa.airport_city = %s and flight.airline_name in (select airline_name from airline_staff where username = %s) \
                            order by departure_time"
                cursor.execute(query, (d_city, a_city,user_id))
            elif s_date == e_date:
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name  and\
                            ad.airport_city = %s and aa.airport_city = %s and \
                            convert(departure_time,date) = %s and flight.airline_name in (select airline_name from airline_staff where username = %s) order by departure_time"
                cursor.execute(query, (d_city, a_city, s_date, user_id))
            else:
                query = "SELECT * FROM flight, airport as ad, airport as aa \
                            WHERE flight.departure_airport = ad.airport_name and \
                            flight.arrival_airport = aa.airport_name  and\
                            ad.airport_city = %s and aa.airport_city = %s and flight.airline_name in (select airline_name from airline_staff where username = %s) and \
                            convert(departure_time,date) between %s and %s order by departure_time"
                cursor.execute(query, (d_city, a_city,user_id, s_date, e_date))

        else:
            query = "SELECT * FROM flight, airport as ad, airport as aa \
                WHERE flight.departure_airport = ad.airport_name and \
                flight.arrival_airport = aa.airport_name and flight.airline_name in (select airline_name from airline_staff where username = %s)\
                order by departure_time"
            cursor.execute(query, (user_id))
        data_got = cursor.fetchall()
        cursor.close()

        return render_template('staff_search_city.html', 
                    d_city = d_city,
                    a_city = a_city,
                    s_date = s_date,
                    e_date = e_date,
                    form = form, 
                    data_got = data_got, 
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# airline staff view infor
@app.route('/staff_view_info/<int:flight_num>', methods = ['GET', 'POST'])
def view_info(flight_num):
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        cursor = conn.cursor()
        query1 = "Select email, airline_name, flight_num, ticket_id, name, phone_number\
                From flight join ticket using (flight_num, airline_name) join purchases using(ticket_id) join customer on(purchases.customer_email=customer.email)\
                where flight.flight_num = %s;"
        cursor.execute(query1, (flight_num))
        data_got = cursor.fetchall()
        cursor.close()
        return render_template('view_info.html', 
                    data_got = data_got, 
                    user_id = user_id, 
                    flight_num = flight_num)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))



# airline staff change flight status
@app.route('/change_status/<int:flight_num>', methods = ['GET', 'POST'])
def change_status(flight_num):
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        # get the user permission
        cursor = conn.cursor()
        query1 = "Select permission_type\
                From permission\
                where username = %s;"
        cursor.execute(query1, (user_id))
        data_got = cursor.fetchall()
        if data_got:
            if 'Operator' in list(list(data_got[i].values())[0] for i in range(len(data_got))):
                # get the airline
                query = "Select airline_name\
                From airline_staff\
                where username = %s;"
                cursor.execute(query, (user_id))
                airline = list(cursor.fetchall()[0].values())[0]


                form = change_status_form()
                status = None
                if form.validate_on_submit():
                    status = form.status.data
                    query1 = "update flight set status=%s where airline_name=%s and flight_num=%s"
                    cursor.execute(query1, (status, airline, flight_num))
                    conn.commit()
                    cursor.close()
                    flash('Change Applied')
                    return render_template('change_status.html', 
                                        form = form, 
                                        status = status,
                                        airline = airline,
                                        user_id = user_id, 
                                        flight_num = flight_num)
                else:
                    return render_template('change_status.html', 
                                        form = form, 
                                        status = status,
                                        airline = airline,
                                        user_id = user_id, 
                                        flight_num = flight_num)

            else:
                flash('Invalid Permission, "Operator" permission is needed for this act')
                return redirect(url_for('staff_home'))
        else:
            flash('No Permission, "Operator" permission is needed for this act')
            return redirect(url_for('staff_home'))
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# get infor for booking agent
@app.route('/infor_booking_agent_staff', methods = ['GET', 'POST'])
def staff_get_booking_agent():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        cursor = conn.cursor()
        query1 = "select email, count(*) as num\
                from ticket join purchases using (ticket_id) join booking_agent using(booking_agent_id) join airline_staff using(airline_name)\
                where airline_staff.username=%s and date_sub(curdate(), interval 1 month)<=purchase_date\
                group by email order by count(*) desc limit 0, 5;"
        cursor.execute(query1, (user_id))
        data1 = cursor.fetchall()

        ## top 5 agents based on yearly # of sold tickets
        query2 = "select email, count(*) as num\
                from ticket join purchases using (ticket_id) join booking_agent using(booking_agent_id) join airline_staff using(airline_name)\
                where airline_staff.username=%s and date_sub(curdate(), interval 1 year)<=purchase_date\
                group by email order by count(*) desc limit 0, 5;"
        cursor.execute(query2, (user_id))
        data2 = cursor.fetchall()

        ## top 5 agents based on yearly commission
        query3 = "select email, sum(price*0.1) as commission\
                from ticket join flight using (flight_num, airline_name) join purchases using(ticket_id) join booking_agent using(booking_agent_id) join airline_staff using(airline_name)\
                where airline_staff.username=%s and date_sub(curdate(), interval 1 year)<=purchase_date\
                group by email order by commission DESC limit 0, 5;"
        cursor.execute(query3, (user_id))
        data3 = cursor.fetchall()
        cursor.close()

        return render_template('staff_get_booking_agent.html', 
                    data1 = data1,
                    data2 = data2, 
                    data3 = data3, 
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))



# get infor for top customer
@app.route('/staff_get_top_customer', methods = ['GET', 'POST'])
def staff_get_top_customer():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        cursor = conn.cursor()
        query1 = "select email, count(*) as num\
                from ticket join purchases using (ticket_id) join airline_staff using(airline_name) , customer \
                where customer.email = purchases.customer_email and airline_staff.username=%s and date_sub(curdate(), interval 1 year)<=purchase_date\
                group by email order by count(*) desc;"
        cursor.execute(query1, (user_id))
        data1 = cursor.fetchall()

        cursor.close()

        return render_template('staff_get_top_customer.html', 
                    data1 = data1,
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# Get the trip history of the customer
@app.route('/customer_detail/<email>', methods = ['GET', 'POST'])
def customer_detail(email):
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        cursor = conn.cursor()
        query1 = "select * \
                from ticket join purchases using (ticket_id) join airline_staff using(airline_name) join flight using(flight_num) \
                where customer_email = %s and airline_staff.username=%s and date_sub(curdate(), interval 1 year)<=purchase_date\
                order by departure_time;"
        cursor.execute(query1, (email ,user_id))
        data1 = cursor.fetchall()
        cursor.close()

        return render_template('customer_detail.html', 
                    email = email,
                    data1 = data1,
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# get the top d_city
@app.route('/customer_detail', methods = ['GET', 'POST'])
def top_destination():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        cursor = conn.cursor()
        # get the airline
        query = "Select airline_name\
                From airline_staff\
                where username = %s;"
        cursor.execute(query, (user_id))
        airline = list(cursor.fetchall()[0].values())[0]

        # get the top d
        # 3month
        query1 = '''select flight.arrival_airport as airport, airport.airport_city as city, count(*) as num
                    from (flight natural join purchases natural join ticket),airport 
                    where flight.arrival_airport = airport.airport_name 
                    and ticket.airline_name = %s
                    and purchases.purchase_date between date_sub(curdate(), interval 3 month) and curdate()
                    group by flight.arrival_airport, airport.airport_city
                    order by count(*) DESC
                    limit 3'''
        cursor.execute(query1, (airline))
        data1 = cursor.fetchall()
        query2 = '''select flight.arrival_airport as airport, airport.airport_city as city, count(*) as num
                    from (flight natural join purchases natural join ticket),airport 
                    where flight.arrival_airport = airport.airport_name 
                    and ticket.airline_name = %s 
                    and purchases.purchase_date between date_sub(curdate(), interval 1 year) and curdate()
                    group by flight.arrival_airport, airport.airport_city
                    order by count(*) DESC
                    limit 3'''
        cursor.execute(query2, (airline))
        data2 = cursor.fetchall()
        cursor.close()

        return render_template('top_des.html', 
                    data1 = data1,
                    data2 = data2,
                    user_id = user_id)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# Sale Report
@app.route('/sale_report', methods = ['GET', 'POST'])
def sale_report():
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        cursor = conn.cursor()
        form = customer_spend_track_form()
        s_date = None
        e_date = None
        data1 = None
        data2 = None
        data3 = None
        data4 = None
        data5 = None
        data6 = None
        if form.validate_on_submit():
            s_date = form.s_date.data
            e_date = form.e_date.data
            query1 = "Select count(distinct ticket_id) as count\
            From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
            Where airline_staff.username = %s and date_sub(curdate(), interval 1 year)<=purchase_date"
            cursor.execute(query1, (user_id))
            data1 = cursor.fetchall()

            # number of tickets sold in 1 month
            query2 = "Select count(distinct ticket_id)\
                    From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
                    Where airline_staff.username = %s and date_sub(curdate(), interval 1 month)<=purchase_date"
            cursor.execute(query2, (user_id))
            data2 = cursor.fetchone()

            query4 = "Select month(purchase_date) as month, count(ticket_id)\
                    From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
                    Where airline_staff.username = %s and year(purchase_date)=year(curdate())\
                    group by month"
            cursor.execute(query4, (user_id))
            data4 = cursor.fetchall()


            query3 = "Select count(distinct ticket_id) as count\
            From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
            Where airline_staff.username = %s and purchase_date between %s and %s"
            cursor.execute(query3, (user_id, s_date,e_date))
            data3 = cursor.fetchall()

            # direct revenue and indirect revenue in last month
            query5 = "Select sum(case when booking_agent_id is null then price else 0 end) as direct_revenue, sum(case when booking_agent_id is null then 0 else price end) as indirect_revenue\
                    From purchases join ticket using(ticket_id) join flight using(flight_num, airline_name) join airline_staff using(airline_name)\
                    Where username=%s and date_sub(curdate(), interval 1 month)<=purchase_date;"
            cursor.execute(query5, (user_id))
            data5 = cursor.fetchall()

            # direct revenue and indirect revenue in last year
            query6 = "Select sum(case when booking_agent_id is null then price else 0 end) as direct_revenue, sum(case when booking_agent_id is null then 0 else price end) as indirect_revenue\
                    From purchases join ticket using(ticket_id) join flight using(flight_num, airline_name) join airline_staff using(airline_name)\
                    Where username=%s and date_sub(curdate(), interval 1 year)<=purchase_date;"
            cursor.execute(query6, (user_id))
            data6 = cursor.fetchall()
            cursor.close()
            return render_template('sale_report.html', 
                    data1 = data1,
                    data2 = data2,
                    data3 = data3,
                    data4 = data4,
                    data5 = data5,
                    data6 = data6,                    
                    user_id = user_id,
                    form = form)



        else:
            query1 = "Select count(distinct ticket_id) as count\
            From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
            Where airline_staff.username = %s and date_sub(curdate(), interval 1 year)<=purchase_date"
            cursor.execute(query1, (user_id))
            data1 = cursor.fetchall()

            # number of tickets sold in 1 month
            query2 = "Select count(distinct ticket_id)\
                    From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
                    Where airline_staff.username = %s and date_sub(curdate(), interval 1 month)<=purchase_date"
            cursor.execute(query2, (user_id))
            data2 = cursor.fetchone()

            query4 = "Select month(purchase_date) as month, count(ticket_id) as count\
                    From ticket join purchases using (ticket_id) join airline_staff using (airline_name)\
                    Where airline_staff.username = %s and year(purchase_date)=year(curdate())\
                    group by month"
            cursor.execute(query4, (user_id))
            data4 = cursor.fetchall()

            # direct revenue and indirect revenue in last month
            query5 = "Select sum(case when booking_agent_id is null then price else 0 end) as direct_revenue, sum(case when booking_agent_id is null then 0 else price end) as indirect_revenue\
                    From purchases join ticket using(ticket_id) join flight using(flight_num, airline_name) join airline_staff using(airline_name)\
                    Where username=%s and date_sub(curdate(), interval 1 month)<=purchase_date;"
            cursor.execute(query5, (user_id))
            data5 = cursor.fetchall()

            # direct revenue and indirect revenue in last year
            query6 = "Select sum(case when booking_agent_id is null then price else 0 end) as direct_revenue, sum(case when booking_agent_id is null then 0 else price end) as indirect_revenue\
                    From purchases join ticket using(ticket_id) join flight using(flight_num, airline_name) join airline_staff using(airline_name)\
                    Where username=%s and date_sub(curdate(), interval 1 year)<=purchase_date;"
            cursor.execute(query6, (user_id))
            data6 = cursor.fetchall()
            cursor.close()
            return render_template('sale_report.html', 
                    data1 = data1,
                    data2 = data2,
                    data3 = data3,
                    data4 = data4,
                    data5 = data5,
                    data6 = data6,                    
                    user_id = user_id,
                    form = form)
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))







#------------------------------Admin Operations--------------------------------------------
# Example


# Add flight 
@app.route('/add_flight', methods = ['GET', 'POST'])
def add_flight():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        # get the user permission
        cursor = conn.cursor()
        query1 = "Select permission_type\
                From permission\
                where username = %s;"
        cursor.execute(query1, (user_id))
        data_got = cursor.fetchall()
        if data_got:
            if 'Admin' in list(list(data_got[i].values())[0] for i in range(len(data_got))):
                # get the airline
                query = "Select airline_name\
                From airline_staff\
                where username = %s;"
                cursor.execute(query, (user_id))
                airline = list(cursor.fetchall()[0].values())[0]
                flight_num = None
                d_port = None
                d_time =  None
                a_port =  None
                a_time =  None
                price =  None
                status =  None
                ticket_num = None
                plane_id =  None
                form = add_flight_form()
                if form.validate_on_submit():
                    status = form.status.data
                    airline = airline
                    flight_num = form.flight_num.data
                    d_port = form.d_port.data
                    d_time =  form.d_time.data
                    a_port =  form.a_port.data
                    a_time =  form.a_time.data
                    price =  form.price.data
                    status =   form.status.data
                    plane_id =  form.plane_id.data
                    ticket_num = form.ticket_num.data
                    # get existing flights:
                    query1 = "SELECT flight_num from flight where airline_name = %s"
                    cursor.execute(query1, (airline))
                    data_got = cursor.fetchall()
                    if data_got:
                        flight_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                    else:
                        flight_lis = []
                    

                    query2 = "SELECT airplane_id from airplane where airline_name = %s"
                    cursor.execute(query2, (airline))
                    data_got = cursor.fetchall()
                    if data_got:
                        plane_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                    else:
                        plane_lis = []

                    if flight_num in flight_lis:
                        flash('The flight already exists!')
                        cursor.close()
                        flight_num = None
                        return render_template('add_flight.html', 
                                            form = form, 
                                            status = status,
                                            airline = airline,
                                            user_id = user_id, 
                                            flight_num = flight_num,
                                            d_port = d_port,
                                            d_time = d_time,
                                            a_port = a_port,
                                            a_time = a_time,
                                            price = price,
                                            plane_id = plane_id,
                                            ticket_num = ticket_num)
                    elif plane_id not in plane_lis:
                        flash('The airplane do not exists!')
                        cursor.close()
                        flight_num = None
                        return render_template('add_flight.html', 
                                            form = form, 
                                            status = status,
                                            airline = airline,
                                            user_id = user_id, 
                                            flight_num = flight_num,
                                            d_port = d_port,
                                            d_time = d_time,
                                            a_port = a_port,
                                            a_time = a_time,
                                            price = price,
                                            plane_id = plane_id,
                                             ticket_num = ticket_num)
                     

                    else:
                        # check the seat number
                        query2 = "SELECT seats from airplane where airline_name = %s and airplane_id = %s"
                        cursor.execute(query2, (airline, str(plane_id)))
                        data_got = cursor.fetchall()
                        if data_got:
                            plane_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                        else:
                            plane_lis = []
                        if plane_lis[0] <  ticket_num:
                                    flash('The ticket number can not be greater than the total seat of the plane!')
                                    cursor.close()
                                    flight_num = None
                                    return render_template('add_flight.html', 
                                            form = form, 
                                            status = status,
                                            airline = airline,
                                            user_id = user_id, 
                                            flight_num = flight_num,
                                            d_port = d_port,
                                            d_time = d_time,
                                            a_port = a_port,
                                            a_time = a_time,
                                            price = price,
                                            plane_id = plane_id,
                                            ticket_num = ticket_num)

                        else:
                            ins = "INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(ins, (airline,flight_num,d_port,d_time,a_port,a_time,price,status,plane_id))
                            conn.commit()
                            cursor.close()
                            for times in range(ticket_num):
                                # get the max ticket_id
                                cursor = conn.cursor()
                                q = 'SELECT max(ticket_id) from ticket where airline_name = %s'
                                cursor.execute(q, (airline))
                                current_t = list(cursor.fetchall()[0].values())[0]
                                if current_t != None:
                                    tid = current_t + 1
                                else:
                                    tid = 1
                                ins2 = "INSERT INTO ticket VALUES(%s, %s, %s)"
                                cursor.execute(ins2, (tid,airline,flight_num))
                                conn.commit()
                                cursor.close()
                            flash('Flight Added.')
                            cursor.close()
                            return render_template('add_flight.html', 
                                                form = form, 
                                                status = status,
                                                airline = airline,
                                                user_id = user_id, 
                                                flight_num = flight_num,
                                                d_port = d_port,
                                                d_time = d_time,
                                                a_port = a_port,
                                                a_time = a_time,
                                                price = price,
                                                ticket_num = ticket_num,
                                                plane_id = plane_id)
                else:
                    cursor.close()
                    return render_template('add_flight.html', 
                                        form = form, 
                                        status = status,
                                        airline = airline,
                                        user_id = user_id, 
                                        flight_num = flight_num,
                                        d_port = d_port,
                                        d_time = d_time,
                                        a_port = a_port,
                                        a_time = a_time,
                                        price = price,
                                        ticket_num = ticket_num,
                                        plane_id = plane_id)


            else:
                flash('Invalid Permission, "Admin" permission is needed for this act')
                return redirect(url_for('staff_home'))
        else:
            flash('No Permission, "Operator" permission is needed for this act')
            return redirect(url_for('staff_home'))
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# Add flight 
@app.route('/add_plane', methods = ['GET', 'POST'])
def add_plane():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        # get the user permission
        cursor = conn.cursor()
        query1 = "Select permission_type\
                From permission\
                where username = %s;"
        cursor.execute(query1, (user_id))
        data_got = cursor.fetchall()
        if data_got:
            if 'Admin' in list(list(data_got[i].values())[0] for i in range(len(data_got))):
                # get the airline
                query = "Select airline_name\
                From airline_staff\
                where username = %s;"
                cursor.execute(query, (user_id))
                airline = list(cursor.fetchall()[0].values())[0]
                plane_id =  None
                seat  = None
                form = add_plane_form()
                if form.validate_on_submit():
                    airline = airline
                    plane_id =  form.plane_id.data
                    seat = form.seat.data
                    # get existing flights:
                    query1 = "SELECT airplane_id from airplane where airline_name = %s"
                    cursor.execute(query1, (airline))
                    data_got = cursor.fetchall()
                    if data_got:
                        flight_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                    else:
                        flight_lis = []
                    if plane_id in flight_lis:
                        flash('The plane already exists!')
                        cursor.close()
                        plane_id = None
                        return render_template('add_plane.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            plane_id = plane_id,
                                            seat = seat)

                    else:
                        ins = "INSERT INTO airplane VALUES(%s, %s, %s)"
                        cursor.execute(ins, (airline,plane_id,seat))
                        conn.commit()
                        flash('Airplane Added.')
                        cursor.close()
                        return render_template('add_plane.html', 
                                            form = form, 
                                            plane_id = plane_id, 
                                            seat = seat)
                else:
                    cursor.close()
                    return render_template('add_plane.html', 
                                            form = form, 
                                            plane_id = plane_id, 
                                            seat = seat)


            else:
                flash('Invalid Permission, "Admin" permission is needed for this act')
                return redirect(url_for('staff_home'))
        else:
            flash('No Permission, "Operator" permission is needed for this act')
            return redirect(url_for('staff_home'))
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# Add airport
@app.route('/add_airport', methods = ['GET', 'POST'])
def add_airport():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        # get the user permission
        cursor = conn.cursor()
        query1 = "Select permission_type\
                From permission\
                where username = %s;"
        cursor.execute(query1, (user_id))
        data_got = cursor.fetchall()
        if data_got:
            if 'Admin' in list(list(data_got[i].values())[0] for i in range(len(data_got))):
                # get the airline
                query = "Select airline_name\
                From airline_staff\
                where username = %s;"
                cursor.execute(query, (user_id))
                airline = list(cursor.fetchall()[0].values())[0]
                port_name =  None
                city  = None
                form = add_port_form()
                if form.validate_on_submit():
                    airline = airline
                    port_name =  form.port_name.data
                    city = form.city.data
                    # get existing ports:
                    query1 = "SELECT airport_name from airport"
                    cursor.execute(query1)
                    data_got = cursor.fetchall()
                    if data_got:
                        flight_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                    else:
                        flight_lis = []
                    if port_name in flight_lis:
                        flash('The airport already exists!')
                        cursor.close()
                        port_name = None
                        return render_template('add_port.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            port_name = port_name,
                                            city = city)

                    else:
                        ins = "INSERT INTO airport VALUES(%s, %s)"
                        cursor.execute(ins, (port_name,city))
                        conn.commit()
                        flash('Airport Added.')
                        cursor.close()
                        return render_template('add_port.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            port_name = port_name,
                                            city = city)
                else:
                    cursor.close()
                    return render_template('add_port.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            port_name = port_name,
                                            city = city)

            else:
                flash('Invalid Permission, "Admin" permission is needed for this act')
                return redirect(url_for('staff_home'))
        else:
            flash('No Permission, "Operator" permission is needed for this act')
            return redirect(url_for('staff_home'))
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# Add booking agent
@app.route('/add_booking_agent', methods = ['GET', 'POST'])
def add_booking_agent():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        # get the user permission
        cursor = conn.cursor()
        query1 = "Select permission_type\
                From permission\
                where username = %s;"
        cursor.execute(query1, (user_id))
        data_got = cursor.fetchall()
        if data_got:
            if 'Admin' in list(list(data_got[i].values())[0] for i in range(len(data_got))):
                # get the airline
                query = "Select airline_name\
                From airline_staff\
                where username = %s;"
                cursor.execute(query, (user_id))
                airline = list(cursor.fetchall()[0].values())[0]
                email=  None
                form = add_ba_form()
                if form.validate_on_submit():
                    airline = airline
                    email = form.email.data
                    # get existing ba:
                    query1 = "SELECT email from booking_agent where email not in (SELECT email from booking_agent_work_for)"
                    cursor.execute(query1)
                    data_got = cursor.fetchall()
                    if data_got:
                        flight_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                    else:
                        flight_lis = []
                    if email not in flight_lis:
                        flash('The booking agent dose not exist or already works for your airline')
                        cursor.close()
                        email = None
                        return render_template('add_booking_agent.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            email = email)

                    else:
                        ins = "INSERT INTO booking_agent_work_for VALUES(%s, %s)"
                        cursor.execute(ins, (email,airline))
                        conn.commit()
                        flash('Booking Agent Added.')
                        cursor.close()
                        return render_template('add_booking_agent.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            email = email)

                else:
                    cursor.close()
                    return render_template('add_booking_agent.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            email = email)


            else:
                flash('Invalid Permission, "Admin" permission is needed for this act')
                return redirect(url_for('staff_home'))
        else:
            flash('No Permission, "Operator" permission is needed for this act')
            return redirect(url_for('staff_home'))
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))


# Grant permission
# Add booking agent
@app.route('/grant_permission', methods = ['GET', 'POST'])
def grant_permission():
    # form = customer_purchase_form()
    user_id = session['user_id']
    if user_id == None:
        flash("Haven't login yet, please try after login")
        return redirect(url_for('index'))
    if user_id == session['user_id']:
        # get the user permission
        cursor = conn.cursor()
        query1 = "Select permission_type\
                From permission\
                where username = %s;"
        cursor.execute(query1, (user_id))
        data_got = cursor.fetchall()
        if data_got:
            if 'Admin' in list(list(data_got[i].values())[0] for i in range(len(data_got))):
                # get the airline
                query = "Select airline_name\
                From airline_staff\
                where username = %s;"
                cursor.execute(query, (user_id))
                airline = list(cursor.fetchall()[0].values())[0]
                user_name = None
                p_type = None
                form = grant_permission_form()
                if form.validate_on_submit():
                    airline = airline
                    user_name = form.user_name.data
                    p_type = form.p_type.data
                    # get existing staff:
                    query1 = "SELECT username from airline_staff where airline_name = %s"
                    cursor.execute(query1, (airline))
                    data_got = cursor.fetchall()
                    if data_got:
                        flight_lis = list(list(data_got[i].values())[0] for i in range(len(data_got)))
                    else:
                        flight_lis = []
                    if user_name not in flight_lis:
                        flash('The staff dose not exist in your airline company.')
                        cursor.close()
                        user_name = None
                        return render_template('grant_permission.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            user_name = user_name,
                                            p_type = p_type)

                    else:
                        ins = "INSERT INTO permission VALUES(%s, %s)"
                        cursor.execute(ins, (user_name,p_type))
                        conn.commit()
                        flash('Now Permission Granted.')
                        cursor.close()
                        return render_template('grant_permission.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            user_name = user_name,
                                            p_type = p_type)

                else:
                    cursor.close()
                    return render_template('grant_permission.html', 
                                            form = form, 
                                            airline = airline,
                                            user_id = user_id, 
                                            user_name = user_name,
                                            p_type = p_type)

            else:
                flash('Invalid Permission, "Admin" permission is needed for this act')
                return redirect(url_for('staff_home'))
        else:
            flash('No Permission, "Operator" permission is needed for this act')
            return redirect(url_for('staff_home'))
    else:
        flash("Invalid User, please try after login")
        return redirect(url_for('index'))










#---------------------------------------------------End----------------------------------------------------------------

if __name__ == "__main__":
	app.run('127.0.0.1', 5500, debug = False)