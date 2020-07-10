import pytest
from src.components.lang.parser import Analyze


# ---- Defining fixtures for testing ---- #

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
    sample = "Salut Grandpy, est ce que tu connais l'adresse " \
             "d'Openclassrooms ?"
    result = Analyze(sample)

    expected_valuable_info = ["Salut", "GrandPy", "connais", "adresse",
                              "OpenClassrooms"]
    expected_greetings = ["Salut"]
    expected_locations = ["OpenClassrooms"]

    assert list(result.valuable_info) == expected_valuable_info
    assert result.found_greetings
    assert result.greetings == expected_greetings
    assert result.found_locations
    assert result.locations == expected_locations




# test get_entities with capsys
