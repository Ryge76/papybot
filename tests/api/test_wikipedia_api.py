import pytest
from src.components.api.wikipedia import Wikipedia


@pytest.fixture(scope='module')
def test_instance():
    test_instance = Wikipedia('Paris')
    return test_instance


# Gloabal test of Wikipedia class
def test_wikipedia_instance(test_instance):
    """Test if Wikipedia class has a non empty dict in its 'infos' attribute
    (thus succeeded in making the call to the API)"""

    expected_extract = "Paris [pa.ʁi]  est la ville la plus peuplée et la capitale de la France.\nElle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien, sur une boucle de la Seine, entre les confluents de celle-ci avec la Marne et l'Oise. Paris est également le chef-lieu de la région Île-de-France et le centre de la métropole du Grand Paris, créée en 2016."

    assert test_instance.infos.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert test_instance.infos.get('extract') == expected_extract


# Following are tests of internal methods of Wikipedia class

# Should return and the integer id of 'Paris' page in Wikipedia
def test_find_page_id(test_instance):
    expected_id = 681159
    assert test_instance.result_page_id == expected_id


# test of internal method of Wikipedia class
def test_api_call(test_instance):
    custom_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": "Paris",
        "srenablerewrites": 1,
        "srsort": "relevance"
    }

    data = test_instance._call_api(custom_params)
    assert isinstance(data, dict)
