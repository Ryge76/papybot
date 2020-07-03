from ..src.components.api.wikipedia import Wikipedia


def test_wikipedia():
    """Test if Wikipedia class has a non empty dict in its 'infos' attribute
    (thus succeeded in making the call to the API)"""

    search = Wikipedia('Paris')
    assert len(search.infos) != 0


