import pytest
import requests

from src.components.api.wikipedia import Wikipedia


# ---- Defining fixtures and mocks used for testing ---- #

def mock_requests_session():
    """ Create fake session object to mock response from API call """
    class FakeSession:
        def __init__(self):
            self.status_code = 200

        def get(self, url, params, timeout):
            return self

        def json(self):
            return {"status": "fake call succeeded !"}

    return FakeSession()


@pytest.fixture()
def mock_wikipedia_instance(monkeypatch):
    """Create fake Wikipedia instance with session attribute containing a
    mocked request.Session object"""

    class FakeWikipedia(Wikipedia):
        def __init__(self):
            monkeypatch.setattr('requests.Session', mock_requests_session)
            self.session = requests.Session()
            self.URL = 'http://'

    return FakeWikipedia()


@pytest.fixture(scope='module')
def global_test_instance():
    test_instance = Wikipedia('Paris')
    return test_instance


# ----- Tests ------ #

# Gloabal test of Wikipedia class
def test_wikipedia_instance(global_test_instance):
    """Test if Wikipedia instance have a 'infos' attribute
    containing url and extract of the page related to the query."""

    expected_extract = "Paris [pa.ʁi]  est la ville la plus peuplée et la capitale de la France.\nElle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016."

    assert global_test_instance.infos.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert global_test_instance.infos.get('extract') == expected_extract


# Following are tests of internal methods of Wikipedia class
def test_find_page_id_for_specific_location(global_test_instance):
    """Should return and the integer id of 'Paris' page in Wikipedia"""
    expected_id = 681159

    assert global_test_instance.result_page_id == expected_id


def test_get_infos_for_specific_location(global_test_instance, page_id=681159):
    """Should return a dictionnary containing the url and extract of a page,
    given its ID"""
    collected_info = global_test_instance._get_infos(page_id)
    expected_extract = "Paris [pa.ʁi]  est la ville la plus peuplée et la capitale de la France.\nElle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016."

    assert isinstance(collected_info, dict)
    assert collected_info.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert collected_info.get('extract') == expected_extract


def test_api_call_for_specific_location(global_test_instance):
    custom_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": "Paris",
        "srenablerewrites": 1,
        "srsort": "relevance"
    }

    data = global_test_instance._call_api(custom_params)
    assert isinstance(data, dict)
    assert 'query' in data.keys()


def test_api_call_on_mock_instance(mock_wikipedia_instance):
    """Should return a dictionnary containing a 'status' key with a success
    message."""
    custom_params = {
        "action": "whatever"
    }

    data = mock_wikipedia_instance._call_api(custom_params)
    assert isinstance(data, dict)
    assert data.get('status') == "fake call succeeded !"
