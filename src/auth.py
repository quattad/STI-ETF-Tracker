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

# creates instance 'bp' of Blueprint object. url_prefix is prepended to all URLS associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


# when request received to /auth/register, calls register view and return value as response
@bp.route('/register', methods=('GET', 'POST'))
def register():  # define register view function
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required!'
        elif not password:
            error = 'Password is required!'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()  # saves changes to the db

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone() # fetch list of dictionaries from db. fetchone method takes first row i.e. first dictionary

        if user is None:
            error = 'User is not registered!'
        elif not check_password_hash(user['password'], password):
            error = 'You have entered an incorrect password.'

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
        # stores dictionary with keys and values corresponding to the headers and row values for particular user
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,))


@bp.route('/logout')
def logout():
    session.clear()  # clear any cookies from the user's browser
    return redirect(url_for('index'))  # return to home page


# create decorator for views that require user to be logged in. such views will be preceded by '@login_required'
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view()  # return generated function
