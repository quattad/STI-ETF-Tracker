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

    stocks = db.execute("SELECT stock_name, stock_ticker, stock_quantity FROM stock WHERE user_id = ?", (user_id,)).fetchall()
    return render_template('stocks/index.html', stocks=stocks)


@bp.route('/add', methods=("GET", "POST"))
# decorator is currently returning a runtime error
# @login_required
def add():
    db = get_db()
    user_id = session.get('user_id')

    if request.method == "POST":
        ticker = request.form["ticker"]
        quantity = request.form["quantity"]
        stock_name = request.form["name"]
        error = None

        if (ticker is None) or (quantity is None):
            error = "Please enter a valid ticker or quantity."
        else:
            if db.execute("SELECT * "
                          "FROM stock "
                          "WHERE stock_ticker = ?", (ticker,)).fetchone() \
                    is None:
                db.execute("INSERT INTO stock (user_id, stock_name, stock_ticker, stock_quantity) "
                           "VALUES (?, ?, ?, ?)", (user_id, stock_name, ticker, quantity))
            else:
                current_quantity = db.execute("SELECT stock_quantity "
                                              "FROM stock "
                                              "WHERE user_id = ? AND stock_ticker = ?", (user_id, ticker)).fetchone()
                new_quantity = current_quantity["stock_quantity"] + int(quantity)
                db.execute("UPDATE stock "
                           "SET stock_quantity = ? "
                           "WHERE user_id = ? AND stock_ticker = ?", (new_quantity, user_id, ticker))
            db.commit()

        return redirect(url_for("stocks.index"))

    elif request.method == "GET":
        return render_template("stocks/add.html")