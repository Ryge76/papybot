import pytest
from src.components.lang.parser import Analyze


# ---- Defining fixtures, mocks, and variables for testing ---- #
@pytest.fixture()
def mock_token():
    class FakeToken:
        def __init__(self, pos=None, lower=None, lemma=None):
            self.pos_ = pos
            self.lower_ = lower
            self.lemma_ = lemma

    return FakeToken

@pytest.fixture()
def mock_entity():
    class FakeEntity:
        def __init__(self, label=None):
            self.label_ = label

    return FakeEntity
# ---- Tests ---- #


# global test for stopwords
sentences_to_try = ["... ? ! ; : .",
                    "Où es-tu ?",
                    "Je suis deja debout."
                    ]


@pytest.mark.parametrize('test_sentence', sentences_to_try)
def test_no_valuable_info_found_for_stopwords(test_sentence):
    """Should not retain valuable word in proposed sentences"""
    result = Analyze(test_sentence)
    assert len(result.valuable_info) == 0


# global test of the class for a specific sentence
def test_parser_on_sample_sentence():
    """Should retain some valuable words from sentence, including 1 location
    and 1 greetings word."""

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


# ---- unit test for methods ---- #


greetings_list = ["bonjour", "bonsoir", "au revoir", "adieu", "salut",
                  "coucou", "hey", "'lut", "hello", "merci", "bonne nuit"]


@pytest.mark.parametrize('checklist', greetings_list)
def test_is_greeting_return_true(mock_token, checklist):
    """Should return True if word is in the greetings list """
    result = Analyze.is_greeting(mock_token(lower=checklist))
    assert result == True


not_greetings_list = ["kikoo", "citron", "porte"]


@pytest.mark.parametrize('checklist', not_greetings_list)
def test_is_greeting_return_false(mock_token, checklist):
    """Should return True if word is in the greetings list """
    result = Analyze.is_greeting(mock_token(lower=checklist))
    assert result == False




@pytest.mark.parametrize('checklist', ["LOC", "GPE", "ORG"])
def test_is_location_return_true(mock_entity, checklist):
    """Should return true for defined entity types"""
    result = Analyze.is_location(mock_entity(label=checklist))
    assert result == True



possible_entity_type = ["PERSON", "NORP", "FAC", "PRODUCT", "EVENT",
                        "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME",
                        "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]


@ pytest.mark.parametrize('checklist', possible_entity_type)
def test_is_location_return_false(mock_entity, checklist):
    """Should return false for all other existing entity types"""
    result = Analyze.is_location(mock_entity(label=checklist))
    assert result == False


@pytest.mark.parametrize('checklist', ["manger", "nager", "rouler"])
def test_is_travel_verb_return_false(mock_token, checklist):
    """Should return false for random verbs"""
    result = Analyze.is_travel_verb(mock_token(lemma=checklist))
    assert result == False


target_verbs = ["aller", "bouger", "bourlinguer", "circuler", "courir",
                "déplacer", "excursionner", "filer", "louvoyer",
                "marcher",
                "naviguer", "nomadiser", "pérégriner", "partir",
                "se balader", "se trouver", "trouver",
                "se déplacer", "se promener", "se transporter",
                "sillonner",
                "transhumer", "vagabonder", "visiter", "voyager",
                "se promoner", "se rendre"]


@pytest.mark.parametrize('checklist', target_verbs)
def test_is_travel_verb_return_false(mock_token, checklist):
    """Should return true for selected verbs"""
    result = Analyze.is_travel_verb(mock_token(lemma=checklist))
    assert result == True


def test_get_entities(capsys):
    test = Analyze("Salut GrandPy ! Est ce que tu connais l'adresse "
            "d'OpenClassrooms ?")

    test.get_entities()
    out, err = capsys.readouterr()
    expected_outcome = "\n Nombre d'entités trouvées: 2.\n\n" \
                       " Entité: Salut GrandPy ! > Etiquette: MISC\n\n" \
                       " Entité: OpenClassrooms > Etiquette: ORG\n"

    assert out == expected_outcome
