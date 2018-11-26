import os
import tempfile

import pytest
from src import create_app
from src.db import get_db, init_db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test"""

    # create temporary file to isolate database for each test.
    db_fd, db_path = tempfile.mkstemp()

    # create app with common test config
    app = create_app({'TESTING': True,
                      'DATABASE': db_path})

    with app.app_context():
        init_db()
        get_db()

    yield app

    # close and remove temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """ Create test client for the app"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create runner for app's click commands"""
    return app.test_cli_runner()


class AuthConfig(object):
    """
    Define class "AuthConfig" that takes current client as an argument with methods and methods that already instantiates
    'login' and 'logout' methods with test username and password
    """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        self._client.post("/auth/login",
                          data={'username': username,
                                'password': password}
                          )

    def logout(self):
        self._client.get('/auth/logout')

    def register(self):
        self._client.post('/auth/register')


@pytest.fixture
def auth(client):
    """ Returns instance of AuthConfig object with configured instance variables and methods"""
    return AuthConfig(client)
