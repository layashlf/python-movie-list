from flask import Blueprint, render_template, request, redirect, url_for, flash,make_response,session
from werkzeug.security import generate_password_hash, check_password_hash
from my_app.controllers.database import open_connection,close_connection
from datetime import datetime, timedelta
authBp = Blueprint('auth', __name__, url_prefix='/auth')

from my_app.util.jwt_util import encode,decode

@authBp.route('/')
def index():
    return "this is base auth route"
@authBp.route('/register', methods=('GET', 'POST'))
def register():
    """
    The `register` function in the Python code snippet handles user registration by validating input
    data, checking for errors, and inserting user information into a database if no errors occur.
    :return: The function `register()` is returning the rendered template 'auth/register.html' if the
    request method is not 'POST'. If the request method is 'POST', it will either redirect to the login
    page if the registration is successful, or it will flash an error message and stay on the
    registration page.
    """

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        error = None

        if password!=confirmPassword:
            flash("Password does not match")
        

        if not name or not email or not password:
            error = 'Please enter all the required fields'
 
        db_obj = open_connection()

        if error is None:
            try:
                cursor = db_obj.cursor()
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                cursor.execute(
                    query,
                    (name, email, generate_password_hash(password)),
                )
                cursor.close()
                db_obj.commit()
            except Exception as e:
                error = str(e)
            else:
                return redirect(url_for("auth.login"))
            finally:
                close_connection()

        flash(error)

        print (f'name={name}, email={email}, password={password}, confirmPassword={confirmPassword}')

    return render_template('auth/register.html')

@authBp.route('/login', methods=('GET', 'POST'))
def login():
    """
    The `login` function in the provided Python code handles user authentication by checking
    credentials, querying the database, and setting a session token upon successful login.
    :return: a response object that redirects the user to the 'movies.list' route if the login is
    successful. If there are any errors during the login process, it will flash the error message and
    render the 'auth/login.html' template for the user to try logging in again.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        error = None

        if not email or not password:
            error = 'Please input your credential'
        
        
        if error is None:
            try:
                db_obj = open_connection()
                cursor = db_obj.cursor()

                query = 'SELECT id, name, email, password FROM users WHERE email = %s'
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if not user:
                    error = 'Invalid credential! no user'

                (user_id, user_name, user_email, user_password) = user

                validate_password = check_password_hash(
                    user_password, password
                )

                if not validate_password:
                    error = 'Invalid credential! password'
                print (error)
                if error is None:
                   

                    payload = {
                        "user_id": user_id,
                        "user_name": user_name,
                        "email": user_email,
                        "exp": datetime.now() + timedelta(hours=1)
                    }
                    session['user'] = payload
                    token = encode(payload)
                    response = make_response(redirect(url_for('movies.list')))
                    response.set_cookie('auth_token', token)
                    return response
            except Exception as e:
                error = 'Unable to login with given credential!'
                print(error,e)
                return make_response(redirect(url_for('auth.login')))
            

                
            finally:
                close_connection()

        flash(error)
        return render_template('auth/login.html')

    return render_template('auth/login.html')


@authBp.route('/logout')
def logout():
    """
    The `logout` function logs the user out by redirecting to the login page, clearing the
    authentication token cookie, and deleting the user session.
    :return: The `logout()` function is returning a response object that redirects the user to the login
    page, clears the 'auth_token' cookie, removes the 'user' key from the session, and then returns the
    response object.
    """
    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie('auth_token', '', expires=0)
    del session['user']
    return response

@authBp.before_app_request
def check_auth():
    """
    The function `check_auth` checks the authentication token and redirects the user based on the
    current route and authentication status.
    :return: The `check_auth()` function returns `None` if none of the conditions for redirecting are
    met.
    """
    current_route = request.endpoint
    auth_token = request.cookies.get('auth_token')
    print(auth_token)

    if auth_token is not None and current_route in ['auth.register', 'auth.login']:
        try:

            if decode(auth_token):
                return redirect(url_for('movies.list'))
        except Exception as e:
            print(e)
    elif auth_token is None and current_route not in ['auth.register', 'auth.login']:
        return redirect(url_for('auth.login'))


    return None