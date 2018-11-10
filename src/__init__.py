import os
from flask import Flask

def create_app(test_config = None):
    # create and configure application
    app = Flask(__name__, instance_relative_config = True)  # tells app that configuration files are relative to instance folder

    # sets some default configurations
    app.config.from_mapping(
        SECRET_KEY='dev',  # overwrite with random value during deployment
        DATABASE=os.path.join(app.instance_path, 'sti-etf-tracker.sqlite')
    )

    if test_config is None:
        # load instance config, if it exists, when not testing. can be used to set actual SECRET_KEY
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in. configure tests independently of other development values
    app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)  # creates instance folder for SQLite database
    except OSError:
        pass

    # default page
    @app.route('/'):
    return 'This is my home page!'

    from . import db

    from . import auth
    db.init_app(app)  # allows db to be called via flask init-db

    app.register_blueprint()  # import and register blueprint from factory

    # Cannot seem to activate.
    # Bookmark 8/11/18 23:55. http://flask.pocoo.org/docs/1.0/tutorial/database/

    return app