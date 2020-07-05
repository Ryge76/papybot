import pytest
from ...src.components.api.wikipedia import Wikipedia


# Check that Wikipedia class throw exceptions on instantiation errors
def test_wikipedia_instance_creation_missing_arg():
    with pytest.raises(TypeError):
        Wikipedia()


def test_wikipedia_instance_empty_query_error():
    with pytest.raises(ValueError):
        Wikipedia('')


# Check handling or errors from wikipedia API
def test_call_api_error_handling():
    pass