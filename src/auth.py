"""
Create blueprint named 'auth.py' that organizes a group of related views and other code.
Views and other code are registered via a blueprint instead of rather than directly in an application.
The blueprint then registers with the application when it is available in the factory function.

This blueprint is for authentication functions.
"""

import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  # creates instance 'bp' of Blueprint object. url_prefix is prepended to all URLS associated with the blueprint

# writing the view code


@bp.route('/register', methods=('GET', 'POST'))  # when request received to /auth/register, calls register view and return value as respponse
def register():  # define register view function
    if request.method() == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()  # fetch database and store in db
        error = None

        if not username:  # checks for case in which username is not defined
            error = 'Username is required!'
        elif not password:  # checks for case in which password is not defined
            error = 'Password is required!'
        elif db.execute('SELECT id FROM user WHERE username = %username', username=username).fetchone() is not None:  # checks for case in which user is already registered. returns one row from the query
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username, password) VALUES (%username, %password)',username=username, password=generate_password_hash(password))
            db.commit()  # saves changes to the db

            return redirect(url_for('auth.login'))

        flash(error)  # print error into the terminal if any

    return render_template('auth.register.html')
