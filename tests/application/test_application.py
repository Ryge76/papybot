import os
import pytest

from src import create_app


# ----- Defining fixtures for testing ---- #

@pytest.fixture
def test_app():
    test_config = {
        'FLASK_ENV': 'development',
        'TESTING': True,
        'FLASK_APP': 'src/papybot.py',
        'GMAPS_KEY': os.environ.get('GMAPS_KEY')
    }

    test_app = create_app(test_config)

    return test_app


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


# ---- tests ---- #

def test_config(test_app):
    """Check if creation of a test instance of the application"""
    assert not create_app().testing
    assert test_app.testing


def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

