import pytest

from ...src.components.api.maps import Gmaps, GmapsModuleError


# ---- Defining fixtures and mocks for testing ---- #

# ---- Tests ---- #


# Global class exception check
def test_empty_query_error():
    with pytest.raises(GmapsModuleError):
        Gmaps().find("")


# test missing or wrong API key
def test_bad_api_key_error():
    fake_key = "123456789ABCDEF"
    test_parameters = {"key": fake_key}

    test_instance = Gmaps()
    test_instance.parameters.update(test_parameters)

    with pytest.raises(GmapsModuleError):
        test_instance.find("Paris")
