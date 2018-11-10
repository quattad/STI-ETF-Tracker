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

