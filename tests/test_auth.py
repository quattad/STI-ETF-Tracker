import src
from src import db

from flask import session, g
import pytest


# define relevant functions for register, login and logout
def register(client, username, password):
    return client.post('auth/register', data=dict(username=username,
                                                  password=password),
                       follow_redirects=True)


def login(client, username, password):
    return client.post('auth/login', data=dict(username=username,
                                               password=password),
                       follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_register(client):
    # test if connection to register page renders without errors
    assert client.get('/auth/register').status_code == 200

    # test that successful registration redirects back to login page
    response = client.post('/auth/register',
                           data={'username': 'test',
                                 'password': 'test'})

    assert response.headers['Location'] == 'http://localhost/auth/login'

    # test that user was successfully added to the table 'user'
    with src.app.app_context():
        assert db.get_db().execute("SELECT * FROM user WHERE username = 'a'").fetchone is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('test', 'passywords', b'You have entered an incorrect password.'),
        ('useryname', 'test', b'User is not registered!')
))
def test_register_validate_input(client, username, password, message):
    response = client.post('/auth/register',
                           data={
                               'username':username,
                               'password':password,
                           }
                           )

    assert message in response.data
