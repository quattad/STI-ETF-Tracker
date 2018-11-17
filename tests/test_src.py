import os
import tempfile
import pytest
import src

@pytest.fixture
def client():
    db_fd, src.app.config['DATABASE'] = tempfile.mkstemp()  # trigger test requests to this application. keep track of cookies
    src.app.config['TESTING'] = True  # activate config flag; disable error catching
    client = src.app.test_client()

    with src.app.app_context():
        src.init_db()

    yield client

    os.close(db_fd)
    os.unlink(src.app.config['DATABASE'])