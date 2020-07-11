import pytest
from src.components.lang.parser import Analyze


# ---- Defining fixtures for testing ---- #
def mock_token():
    class FakeToken:
        def __init__(self):
            self.pos_ = ""

    return FakeToken()

# ---- Tests ---- #

# test stopwords
sentences_to_try = ["... ? ! ; : .",
                    "Où es-tu ?",
                    "Je suis deja debout."
                    ]


@pytest.mark.parametrize('test_sentence', sentences_to_try)
def test_no_valuable_info_found_for_stopwords(test_sentence):
    result = Analyze(test_sentence)
    assert len(result.valuable_info) == 0


# test for a specific sentence
def test_parser_on_sample_sentence():
    sample = "Salut Grandpy ! Est ce que tu connais l'adresse " \
             "d'Openclassrooms ?"
    result = Analyze(sample, True)

    # spacy library parse and convert any sentence in tokens objects with a
    # text attribute containing the word it represents in the sentence.
    result_valuable_info = [token.text for token in result.valuable_info]
    result_greetings = [token.text for token in result.greetings]
    result_locations = [token.text for token in result.locations]

    expected_valuable_info = ["Salut", "Grandpy", "connais", "adresse",
                              "Openclassrooms"]
    expected_greetings = ["Salut"]
    expected_locations = ["Openclassrooms"]

    assert result_valuable_info == expected_valuable_info
    assert result.found_greetings == True
    assert result_greetings == expected_greetings
    assert result.found_locations == True
    assert result_locations == expected_locations

