import pytest
import requests
from src.components.api.wikipedia import Wikipedia, WikipediaModuleError


# ---- Defining fixtures and mocks used for testing ---- #

@pytest.fixture(scope='module')
def global_test_instance():
    """Create an instance initialized on a Paris search."""
    test_instance = Wikipedia('Paris')
    return test_instance


def mock_requests_session():
    """ Create fake session object to mock response from API call """
    class FakeSession:
        def __init__(self):
            self.status_code = 400

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

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


# ----- Tests --------- #

# Check that Wikipedia class throw exceptions on instantiation errors
def test_wikipedia_instance_creation_with_missing_arg_error():
    with pytest.raises(TypeError):
        Wikipedia()


# Check Wikipedia throw an exception if query is empty
def test_wikipedia_instance_empty_query_error():
    """Should raise a class specific error if instantiated with an
    empty string."""

    with pytest.raises(WikipediaModuleError):
        Wikipedia('')


# Check handling of failing connection to wikipedia API
def test_call_api_error_handling(global_test_instance):
    """Should raise o specific class error as requested site is unavailable"""
    # modify URL of the test instance
    global_test_instance.URL = 'http://fake-address.io'

    test_parameters_for_call = {
            "action": "whatever"
        }

    with pytest.raises(WikipediaModuleError):
        global_test_instance._call_api(test_parameters_for_call)


# Check handling of failing connection to wikipedia API
def test_call_api_error_handling2(mock_wikipedia_instance):
    """Should raise a Wkipedia Error since fake response.status.code is 400"""
    test_parameters_for_call = {
            "action": "whatever"
        }

    with pytest.raises(WikipediaModuleError):
        mock_wikipedia_instance._call_api(test_parameters_for_call)


# Check handling of error in the response from wikipedia API
def test_call_api_http_error(global_test_instance):
    """Should raise a class specific error message as query to site is
    incorrect"""
    test_parameters_for_call = {
            "action": "fake_action",
            "format": "json"
        }

    with pytest.raises(WikipediaModuleError):
        global_test_instance._call_api(test_parameters_for_call)
