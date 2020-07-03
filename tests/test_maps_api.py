import pytest
from ..src.components.api.maps import Gmaps


# Global class test
def test_maps_api():
    location = Gmaps()
    location.get('Openclassrooms')
    assert location.about_query[0].get('place_id') == 'ChIJIZX8lhRu5kcRGwYk8Ce3Vc8'


def test_maps_error():
    """Check if bad query is catched by function"""
    with pytest.raises(Exception):
        Gmaps().get('')

