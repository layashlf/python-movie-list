from flask import Blueprint, render_template, request, redirect, url_for, flash

usersBp = Blueprint('auth', __name__, url_prefix='/auth')

@usersBp.route('/')
def index():
    return "this is base auth route"
@usersBp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        print (f'name={name}, email={email}, password={password}')

    return render_template('templates/auth/register.html')

