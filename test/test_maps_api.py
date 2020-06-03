from ..components.maps import Gmaps


def test_gmaps_api():
    response = Gmaps('paris')
    assert response[id] == 1233

