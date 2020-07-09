import pytest
from ...src.components.api.maps import Gmaps, GmapsModuleError


# ---- Defining fixtures and mocks for testing ---- #

@pytest.fixture()
def mock_gmaps_class_with_wrong_key():
    class FakeGmaps(Gmaps):
        GMAPS_KEY = "BadKey"

    return FakeGmaps


# ---- Tests ---- #


# Global class exception check
def test_empty_query_error():
    with pytest.raises(GmapsModuleError):
        Gmaps().get('')


# test missing or wrong API key
def test_bad_api_key_error(mock_gmaps_class_with_wrong_key):
    with pytest.raises(GmapsModuleError):
        mock_gmaps_class_with_wrong_key()


