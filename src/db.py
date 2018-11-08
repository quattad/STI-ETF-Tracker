import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:  # g stores data for a unique request to prevent multiple requests to database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # current_app points to flask application handling request
            detect_types=sqlite3.PARSE.DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()  # returns a database connection

    with current_app.open_resource('schema.sql') as f:  # opens file relative to package
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear existing data and create new tables"""
    init_db()
    click.echo('Initialize database')  # defines command line command that calls init-db function

def init_app(app):
    app.teardown_appcontext(close_db)  # inform Flask to call function when cleaning up and returning response
    app.cli.add_command(init_db_command)  # add new command to be called with Flask command