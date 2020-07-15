from .components.lang.parser import Analyze
from .components.api.wikipedia import Wikipedia, WikipediaModuleError
from .components.api.maps import Gmaps, GmapsModuleError


def analyze_query(query):
    """Analyse user input to get relevant information.
    Return a dict with specifics words for research on Google maps and
    Wikipedia or for creating the bot'sentences."""

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
        analysis.update({"location": False})
        return analysis

    if len(parser_analysis.locations) > 1:
        analysis.update({"location": True,
                         "notsure": True,
                        "notsure_search": parser_analysis.locations[0].text})
        return analysis

    else:
        analysis.update({"look_for": parser_analysis.locations[0].text})
        return analysis

def search_external_services(results_collector, keyword):
    """Contact Wikipedia and Google Maps for a specific keyword."""
    try:
        maps_results = Gmaps().find(keyword)

    except GmapsModuleError:

        results_collector.update({"gmaps": None})

    else:
        results_collector.update({"gmpas": maps_results})

    try:
        wikipedia_results = Wikipedia(keyword).infos

    except WikipediaModuleError:

        results_collector.update({"wikipedia": None})

    else:
        results_collector.update({"wikipedia": wikipedia_results})

    return results_collector


def make_decision(query):
    """Gather informations about user's query, using a parser and external
    services (Google Maps and Wikipedia)"""
    parser_analysis = analyze_query(query)

    if parser_analysis.get('rephrase'):
        return parser_analysis

    if parser_analysis.get('notsure'):
        final_decision = search_external_services(parser_analysis,
                                                  keyword=parser_analysis.get(
            'notsure_search'))

        return final_decision

    else:
        final_decision = search_external_services(parser_analysis,
                                                  keyword=parser_analysis.get('look_for'))

        return final_decision


