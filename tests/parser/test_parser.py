import pytest
from ...src.components.lang.parser import Analyze


# ---- Defining fixtures, mocks, and variables for testing ---- #
@pytest.fixture()
def mock_token():
    class FakeToken:
        def __init__(self, pos=None, lower=None, lemma=None, text=None):
            self.pos_ = pos
            self.lower_ = lower
            self.lemma_ = lemma
            self.text = text

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
    assert result.found_greetings
    assert result_greetings == expected_greetings
    assert result.found_locations
    assert result_locations == expected_locations


# ---- unit test for methods ---- #


greetings_list = ["bonjour", "bonsoir", "au revoir", "adieu", "salut",
                  "coucou", "hey", "'lut", "hello", "merci", "bonne nuit"]


@pytest.mark.parametrize('checklist', greetings_list)
def test_is_greeting_return_true(mock_token, checklist):
    """Should return True if word is in the greetings list """
    result = Analyze.is_greeting(mock_token(lower=checklist))
    assert result


not_greetings_list = ["kikoo", "citron", "porte"]


@pytest.mark.parametrize('checklist', not_greetings_list)
def test_is_greeting_return_false(mock_token, checklist):
    """Should return True if word is in the greetings list """
    result = Analyze.is_greeting(mock_token(lower=checklist))
    assert not result




@pytest.mark.parametrize('checklist', ["LOC", "GPE", "ORG"])
def test_is_location_return_true(mock_entity, checklist):
    """Should return true for defined entity types"""
    result = Analyze.is_location(mock_entity(label=checklist))
    assert result



possible_entity_type = ["PERSON", "NORP", "FAC", "PRODUCT", "EVENT",
                        "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME",
                        "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]


@ pytest.mark.parametrize('checklist', possible_entity_type)
def test_is_location_return_false(mock_entity, checklist):
    """Should return false for all other existing entity types"""
    result = Analyze.is_location(mock_entity(label=checklist))
    assert not result


@pytest.mark.parametrize('checklist', ["manger", "nager", "rouler"])
def test_is_travel_verb_return_false(mock_token, checklist):
    """Should return false for random verbs"""
    result = Analyze.is_travel_verb(mock_token(lemma=checklist))
    assert not result


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
    assert result


def test_get_entities_return_entities(capsys):
    """Should find 2 entities in the sample sentence"""
    test = Analyze("Salut GrandPy ! Est ce que tu connais l'adresse "
            "d'OpenClassrooms ?")

    test.get_entities()
    out, err = capsys.readouterr()
    expected_outcome = "\n Nombre d'entités trouvées: 2.\n\n" \
                       " Entité: Salut GrandPy ! > Etiquette: MISC\n\n" \
                       " Entité: OpenClassrooms > Etiquette: ORG\n"

    assert out == expected_outcome


def test_get_valuable_info(capsys):
    test = Analyze("Où se trouve la Tour Eiffel ?")

    expected_outcome = "\n Phrase initiale: Où se trouve la Tour Eiffel ?. " \
                       "\n Mots retenus: [trouve, Tour, Eiffel]\n"

    test.get_valuable_info()

    out, err = capsys.readouterr()

    assert out == expected_outcome

def test_check_greetings_return_no_greetings(capsys):
    """Shouldn't find greetings word and have false for the greetings_found
    attribute."""
    test = Analyze("Où se trouve la Tour Eiffel ?")

    with capsys.disabled():
        test.get_valuable_info()  # prevent capture of the output of this step

    test.check_greetings()
    out, err = capsys.readouterr()

    assert out == "Pas de mots de saluation dans la phrase.\n"
    assert not test.found_greetings


def test_check_greetings_find_greetings(capsys):
    """Should find a greeting word and have true for the greetings_found
    attribute."""
    test = Analyze("Bonjour, où se trouve la Tour Eiffel ?")

    with capsys.disabled():
        test.get_valuable_info()  # prevent capture of the output of this step

    test.check_greetings()
    out, err = capsys.readouterr()

    assert out == "Salutation trouvée: [Bonjour] \n"
    assert test.found_greetings


def test_check_location_not_found():
    """Shouldn't return any location"""
    test = Analyze("Bonjour, comment ça va ?")
    result = test.check_location()

    assert result == None
    assert not test.found_locations


def test_check_location_find_entities(capsys):
    """Should find the location in the sample sentence"""
    test = Analyze("Où se trouve la Tour Eiffel ?")
    test.check_location()

    out, err = capsys.readouterr()
    expected_outcome = "\n Lieu(x) trouvé(s): [Tour Eiffel]\n"

    assert out == expected_outcome
    assert test.found_locations


def test_check_travel_verb_not_found():
    """Shouldn't find any verb related to a travel intention"""
    test = Analyze("Je veux nager à la plage.")
    test.get_valuable_info()
    result = test.check_travel_verb()

    assert result == None
    assert not test.found_travel_verbs

def test_check_travel_verb_found(capsys):
    """Shouldn't find any verb related to a travel intention"""
    test = Analyze("Je veux visiter Paris.")
    with capsys.disabled():
        test.get_valuable_info()

    test.check_travel_verb()
    out, err = capsys.readouterr()

    expected_outcome = "Verbe(s) trouvé(s): [visiter] \n"

    assert out == expected_outcome
    assert test.found_travel_verbs


def test_parse_noun_chuncks(capsys):
    """Should find related noun chuncks."""
    test = Analyze("Où se trouve la Tour Eiffel ?")
    test.parse_noun_chunks()

    out, err = capsys.readouterr()
    expected_outcome = "Groupe nominal:  la Tour Eiffel  >> racine du " \
                       "groupe:  Tour  > role:  obj  > racine dans " \
                       "la phrase:  trouve\n"

    assert out == expected_outcome