import pytest
import requests
from src.components.api.wikipedia import Wikipedia, WikipediaModuleError


@pytest.fixture(scope='module')
def test_instance():
    test_instance = Wikipedia('Paris')
    return test_instance


# Check that Wikipedia class throw exceptions on instantiation errors
def test_wikipedia_instance_creation_missing_arg():
    with pytest.raises(TypeError):
        Wikipedia()


def test_wikipedia_instance_empty_query_error():
    with pytest.raises(WikipediaModuleError):
        Wikipedia('')


# Check handling or failing connection from wikipedia API
@pytest.mark.xfail(reason='Exception handled')
def test_call_api_error_handling(global_test_instance):
    # modify URL of the test instance
    global_test_instance.URL = 'http://fake-address.io'

    test_parameters_for_call = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "srsearch": "Paris",
            "srenablerewrites": 1,
            "srsort": "relevance"
        }
    with pytest.raises(requests.exceptions.RequestException):
        global_test_instance._call_api(test_parameters_for_call)


# Check handling of error in the response from wikipedia API
# @pytest.mark.xfail(reason='Exception handled')
def test_call_api_http_error(global_test_instance):
    test_parameters_for_call = {
            "action": "fake_action",
            "format": "json"
        }

    with pytest.raises(WikipediaModuleError):
        global_test_instance._call_api(test_parameters_for_call)


