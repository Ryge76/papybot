from ...src.utils import make_decision, analyze_query


# ---- Defining fixtures, mocks and variables for testing ---- #

analysis_results_protype = {"greetings": False,
                        "greeting_word": "",
                        "rephrase": False,
                        "notsure": False,
                        "notsure_search": "",
                        "searched_word": "",
                        "gmaps": "",
                        "wikipedia": ""}

analysis_results_step1 = {"greetings": True,
                        "greeting_word": "Salut"}

analysis_results_case1 = {"greetings": True,
                        "greeting_word": "Salut",
                          "look_for": "Openclassrooms",
                          "rephrase": False}

analysis_results_case2 = {"greetings": False,
                          "rephrase": True}

analysis_results_case3 = {}

def test_analyze_query():
    result = analyze_query("Salut Papybot ! Où se trouve Openclassrooms ?")

    expected_result = analysis_results_case1

    assert result == expected_result

    result2 = analyze_query("A deja")
    expected_result2 = analysis_results_case2

    assert result2 == expected_result2


def test_make_decision():
    result = make_decision("Salut Papybot ! Où se trouve Openclassrooms ?")

    expected_result = analysis_results_protype

    assert result == expected_result

