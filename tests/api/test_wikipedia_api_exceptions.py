import pytest
import requests.exceptions
from ...src.components.api.wikipedia import Wikipedia, WikipediaModuleError


# ---- Defining fixtures and mocks used for testing ---- #

sample_response_with_error = {
    "error": {
        "code": "badvalue",
        "info": 'Unrecognized value for parameter "action": fake_action.',
        "*": "See https://fr.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes.",
    },
    "servedby": "mw1345",
}


@pytest.fixture
def wikipedia_test_instance():
    return Wikipedia("test", auto=False)


@pytest.fixture
def mock_response():
    """ Create fake response object. """

    class FakeResponse:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        def get(self, url, params, timeout):
            return self

        def json(self):
            return sample_response_with_error

    return FakeResponse()


def mock_requests_session():
    """ Create fake session object. """

    class FakeSession:
        def __init__(self):
            self.status_code = 400

        def raise_for_status(self):
            raise requests.exceptions.HTTPError

        def get(self, url, params, timeout):
            return self

        def json(self):
            return sample_response_with_error

    return FakeSession()


@pytest.fixture
def mock_wiki_instance(monkeypatch):
    """Create Wikipedia instance with 'session' attribute containing a
    mocked request.Session object"""

    monkeypatch.setattr("requests.Session", mock_requests_session)
    instance = Wikipedia("test", auto=False)

    return instance


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
        Wikipedia("")


# Check handling of failing connection to wikipedia API
def test_call_api_unreachable_api_error(wikipedia_test_instance):
    """Should raise o specific class error as requested site is unavailable"""
    # modify URL of the test instance to fake api out of reach
    wikipedia_test_instance.URL = "http://fake-address.io"

    test_parameters_for_call = {"action": "whatever"}

    with pytest.raises(requests.exceptions.RequestException):
        wikipedia_test_instance._call_api(test_parameters_for_call)


# Check handling of failing connection to wikipedia API
def test_call_api_http_error(mock_wiki_instance):
    """Should raise a Wkipedia Error since fake response.status.code is 400"""
    test_parameters_for_call = {"action": "whatever"}

    with pytest.raises(requests.exceptions.HTTPError):
        mock_wiki_instance._call_api(test_parameters_for_call)


# Check handling of error in the response from wikipedia API
def test_get_data_from_response_error(wikipedia_test_instance, mock_response):
    """Should raise a class specific error message as query to site is
    incorrect"""

    with pytest.raises(requests.exceptions.HTTPError):
        wikipedia_test_instance._get_data_from_response(mock_response)
