import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure application
    app = Flask(__name__, instance_relative_config=True)   # tells app that configuration files are relative to instance folder

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

    from . import db
    db.init_app(app)  # allows db to be called via flask init-db

    from . import auth
    app.register_blueprint(auth.bp)  # import and register blueprint 'auth' from factory

    from . import stocks
    app.register_blueprint(stocks.bp)
    app.add_url_rule('/', endpoint='index')  # associates endpoint name 'index' with / url. see comments above.

    return app


if __name__ == "__main__":
    create_app()
