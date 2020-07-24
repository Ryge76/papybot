import os
import pytest

from src import create_app


# ----- Defining fixtures for testing ---- #


@pytest.fixture
def test_app():
    test_config = {
        "FLASK_ENV": "development",
        "TESTING": True,
        "FLASK_APP": "src/papybot.py",
        "GMAPS_KEY": os.environ.get("GMAPS_KEY"),
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
    response = test_client.get("/")
    assert response.status_code == 200


def test_search(test_client):
    test_data = {"query": "Où se trouve Openclassrooms"}
    expected_result = {
        "greetings": False,
        "rephrase": False,
        "location": True,
        "look_for": "Openclassrooms",
        "gmaps": {
            "address": "7 Cité Paradis, 75010 Paris, France",
            "coord": {"lat": 48.8748465, "lng": 2.3504873},
        },
        "wikipedia": {
            "extract": "OpenClassrooms est un site web de formation en ligne qui propose à ses membres des cours certifiants et des parcours débouchant sur des métiers en croissance. Ses contenus sont réalisés en interne, par des écoles, des universités, des entreprises partenaires comme Microsoft ou IBM, ou historiquement par des bénévoles. Jusqu'en 2018, n'importe quel membre du site pouvait être auteur, via un outil nommé « interface de rédaction » puis « Course Lab ».",
            "url": "https://fr.wikipedia.org/wiki/OpenClassrooms",
        },
    }

    with test_client as c:
        response = c.post("/search/", json=test_data)
        json_data = response.get_json()

        assert json_data == expected_result
