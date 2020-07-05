import pytest
from ...src.components.api.maps import Gmaps


# Global class exception check
def test_maps_error():
    """Check if bad queries are catched by function"""
    with pytest.raises(Exception):
        Gmaps().get('')

