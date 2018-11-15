"""
Create blueprint named 'blog.py' that allows users to see all posts, allow logged in users to create posts and allow
author of post to edit/delete a post.
Views and other code are registered via a blueprint instead of rather than directly in an application.
The blueprint then registers with the application when it is available in the factory function.

This blueprint is for blog-related functions.
However, it will be adapted to the needs of the STI-ETF project later on.
-----------------------------------------------------------------------------------------------------------
General steps to creating blueprints
1) Define blueprint (e.g. blog.py) and register it in the application factory

2) Import and register blueprint from factory using app.register_blueprint() and place the new code near the end of the
factory function before returning the app.
Possible to define a separate index using url_prefix, but if this is the main page then it should be the main index.
Other views will be named accordingly e.g. add view at /add
If there are several views that point to several indexes (e.g. blog.index, plain index endpoint), use
app.add_url_rule() to associate endpoint name 'index' with / so all url_for('name.index') will always redirect to /
URL.
If a separate index view is desired, give blueprint a url_prefix and define separate index view in application factory.
"""

from flask import (Blueprint, Flask, g, redirect, render_template, request, url_for, session)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('stocks', __name__)  # creates a Blueprint object with name "blog"


@bp.route('/')  # show information from both user and stock tables
def index():
    db = get_db()
    user_id = session.get('user_id')

    stocks = db.execute("SELECT * FROM user JOIN stock ON user.id = stock.user_id WHERE user.id = ?", (user_id,))  # used to have fetchall method here. currently returns syntax error

    return render_template('stocks/index.html', stocks=stocks)


@bp.route('/add', methods=("GET", "POST"))
# @login_required  # add decorator to check that user is logged in. if not, redirect
def add():
    if request.method == "POST":
        ticker = request.method.get("ticker")
        quantity = request.method.get("quantity")
        error = None

        if (ticker is None) or (quantity is None):
            error = "Please enter a valid ticker or quantity."
        else:
            db = get_db()
            db.execute("INSERT INTO stock (user.id, stock_ticker, stock_qty) VALUES (? ? ?)", (g.user['id'], ticker, quantity))
            db.commit()
            return redirect(url_for("stocks.index"))

    elif request.method == "GET":
        return render_template("stocks/add.html")