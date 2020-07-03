from ..src.components.api.wikipedia import Wikipedia


# Gloabal test of Wikipedia class
def test_wikipedia():
    """Test if Wikipedia class has a non empty dict in its 'infos' attribute
    (thus succeeded in making the call to the API)"""

    search = Wikipedia('Paris')
    assert len(search.infos) != 0
    assert search.infos.get('url') == 'https://fr.wikipedia.org/wiki/Paris'
    assert len(search.infos.get('extract')) != 0


# unit test of Wikipedia class
def test_api_call():
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": "Paris",
        "srenablerewrites": 1,
        "srsort": "relevance"
    }

    data = Wikipedia('Paris')._call_api(search_params)
    assert isinstance(data, dict)
