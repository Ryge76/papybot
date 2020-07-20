from ...src.utils import make_decision, analyze_query


# ---- Defining fixtures, mocks and variables for testing ---- #

analysis_results_protype = {'gmaps': {'address': '7 Cité Paradis, '
                                                 '75010 Paris, France',
           'coord': {'lat': 48.8748465, 'lng': 2.3504873}},
 'greeting_word': 'Salut',
 'greetings': True,
                            'location': True,
 'look_for': 'Openclassrooms',
 'rephrase': False,
 'wikipedia': {'extract': 'OpenClassrooms est un site web de formation en '
                          'ligne qui propose à ses membres des cours '
                          'certifiants et des parcours débouchant sur des '
                          'métiers en croissance. Ses contenus sont réalisés '
                          'en interne, par des écoles, des universités, des '
                          'entreprises partenaires comme Microsoft ou IBM, ou '
                          "historiquement par des bénévoles. Jusqu'en 2018, "
                          "n'importe quel membre du site pouvait être auteur, "
                          'via un outil nommé « interface de rédaction » puis '
                          '« Course Lab ».',
               'url': 'https://fr.wikipedia.org/wiki/OpenClassrooms'}}


analysis_results_case1 = {"greetings": True,
                        "greeting_word": "Salut",
                          "location": True,
                          "look_for": "Openclassrooms",
                          "rephrase": False}

analysis_results_case2 = {"greetings": False,
                          "rephrase": True}

analysis_results_case3 = {"greetings": False,
                          "location": True,
                          "notsure": True,
                          "notsure_search": "Paris",
                          "rephrase": False}

def test_analyze_query():
    result = analyze_query("Salut Papybot ! Où se trouve Openclassrooms ?")

    expected_result = analysis_results_case1

    assert result == expected_result

    result2 = analyze_query("A deja")
    expected_result2 = analysis_results_case2

    assert result2 == expected_result2

    result3 = analyze_query("Aller à Paris ou aller à Londres ?")
    expected_result3 = analysis_results_case3

    assert result3 == expected_result3


def test_make_decision():
    result = make_decision("Salut Papybot ! Où se trouve Openclassrooms ?")

    expected_result = analysis_results_protype

    assert result == expected_result

