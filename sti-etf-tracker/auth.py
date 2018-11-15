"""
Create blueprint named 'auth.py' that organizes a group of related views and other code.
Views and other code are registered via a blueprint instead of rather than directly in an application.
The blueprint then registers with the application when it is available in the factory function.

This blueprint is for authentication functions.
"""

import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  # creates instance 'bp' of Blueprint object. url_prefix is prepended to all URLS associated with the blueprint

# writing the view code


@bp.route('/register', methods=('GET', 'POST'))  # when request received to /auth/register, calls register view and return value as respponse
def register():  # define register view function
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()  # fetch database and store in db
        error = None

        if not username:  # checks for case in which username is not defined
            error = 'Username is required!'
        elif not password:  # checks for case in which password is not defined
            error = 'Password is required!'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:  # checks for case in which user is already registered. returns one row from the query
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()  # saves changes to the db

            return redirect(url_for('auth.login'))  # endpoint should be 'auth.login' since login is within the 'auth' blueprint

        flash(error)  # print error into the terminal if any

    return render_template('auth/register.html')  # for GET method, redirect to register page


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()  # fetch database and store in db
        error = None  # set default value for error as none

        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone() # fetch list of dictionaries from db. fetchone method takes first row i.e. first dictionary

        if user is None:
            error = 'User is not registered!'
        elif not check_password_hash(user['password'], password):
            error = 'You have entered an incorrect password'

        if error is None:
            session.clear()  # session is dict that stores data across request. data stored in cookie that is sent to the browser. browser sends back with subsequent request. Flask signs data to avoid tampering.
            session['user_id'] = user['id']  # store user id in current session
            return redirect(url_for('index'))  # return to home page

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:  # user logging in for the first time
        g.user = None  # g lasts for the length of the request
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,))  # stores dictionary with keys and values corresponding to the headers and row values for particular user


@bp.route('/logout')
def logout():
    session.clear()  # clear any cookies from the user's browser
    return redirect(url_for('index'))  # return to home page


# create decorator for views that require user to be logged in. such views will be preceded by '@login_required'
def login_required(view):
    @functools.wraps(view)  # wrap original view function
    def wrapped_view(**kwargs):  # modify view function with added function wrapped_view to check if login dictionary exists
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view()  # return generated function
