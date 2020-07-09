import pytest
import requests

from src.components.api.wikipedia import Wikipedia


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


# Gloabal test of Wikipedia class
# Attribute 'infos' should contains url and extract of the page related to the
# query
def test_wikipedia_instance(global_test_instance):
    """Test if Wikipedia class has a non empty dict in its 'infos' attribute
    (thus succeeded in making the call to the API)"""

    expected_extract = "Paris [pa.ʁi]  est la ville la plus peuplée et la capitale de la France.\nElle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016."

    assert global_test_instance.infos.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert global_test_instance.infos.get('extract') == expected_extract

# Following are tests of internal methods of Wikipedia class


# Should return and the integer id of 'Paris' page in Wikipedia
def test_find_page_id_for_specific_location(global_test_instance):
    expected_id = 681159

    assert global_test_instance.result_page_id == expected_id


# Should return a dictionnary containing the url and extract of a page,
# given its ID
def test_get_infos_for_specific_location(global_test_instance, page_id=681159):
    collected_info = global_test_instance._get_infos(page_id)
    expected_extract = "Paris [pa.ʁi]  est la ville la plus peuplée et la capitale de la France.\nElle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016."

    assert isinstance(collected_info, dict)
    assert collected_info.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert collected_info.get('extract') == expected_extract


# test of internal method of Wikipedia class
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


# test of internal method of Wikipedia class
def test_api_call_on_fake_instance(mock_wikipedia_instance):
    custom_params = {
        "action": "whatever"
    }

    data = mock_wikipedia_instance._call_api(custom_params)
    assert isinstance(data, dict)
    assert data.get('status') == "fake call succeeded !"