import pytest
from ...src.components.api.maps import Gmaps


# ---- Defining fixtures and mocks for testing ---- #
@pytest.fixture()
def mock_googlemaps():
    """mock of googlemaps services"""
    class Googlemaps:
        def geocode(self, useless_query):
            return [{'formatted_address': 'fake address',
                    'geometry': {'location': 'nowhere'}
                     }]

    return Googlemaps()


@pytest.fixture()
def fake_gmaps_instance(mock_googlemaps):
    class FakeGmaps(Gmaps):
        def __init__(self):
            self.gmaps_service = mock_googlemaps
            self.about_query = []

    return FakeGmaps()


# ---- Tests ---- #

# Global class test
def test_maps_api():
    location = Gmaps()
    result = location.get('Openclassrooms')
    assert location.about_query[0].get('place_id') == 'ChIJIZX8lhRu5kcRGwYk8Ce3Vc8'
    assert result.get('address') == '7 Cité Paradis, 75010 Paris, France'
    assert result.get('coord') == {'lat': 48.8748465, 'lng': 2.3504873}


# unit test of get function
def test_get_of_maps_api(fake_gmaps_instance):
    """Should return a dictionnary containing fake data"""
    tested_result = fake_gmaps_instance.get('somewhere')

    assert tested_result.get('address') == 'fake address'
    assert tested_result.get('coord') == 'nowhere'
