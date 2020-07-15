from .components.lang.parser import Analyze
from .components.api.wikipedia import Wikipedia
from .components.api.maps import Gmaps


def analyze_query(query):
    parser_analysis = Analyze(query)

    analysis = {}

    if parser_analysis.found_greetings:
        analysis.update({"greetings": True,
                    "greeting_word": parser_analysis.greetings[0].text})

    else:
        analysis.update({"greetings": False})

    if len(parser_analysis.entities) == 0:
        analysis.update({"rephrase": True})
        return analysis

    else:
        analysis.update({"rephrase": False})

    if not parser_analysis.found_locations:
        analysis.update({"nolocation": True})
        return analysis

    if len(parser_analysis.locations) == 0:
        analysis.update({"nolocation": True})
        return analysis

    if len(parser_analysis.locations) > 1:
        analysis.update({"nolocation": False,
                         "notsure": True,
                        "notsure_search": parser_analysis.locations[0]})
        return analysis

    else:
        analysis.update({"look_for": parser_analysis.locations[0].text})
        return analysis



def make_decision(query):
    parser_analysis = analyze_query(query)
