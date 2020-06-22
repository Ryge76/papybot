from flask import render_template, request, make_response
from .config import GMAPS_KEY
from . import create_app

from .components.lang import parser
from .components.api import gmaps
from .components.api import wikipedia

app = create_app()


@app.route('/')
def index():
    if request.method == 'POST':
        return render_template('index.html', key=GMAPS_KEY)
    else:
        return render_template('index.html', key=GMAPS_KEY)


@app.route('/search/', methods=['POST'])
def search():

    analysis_results = {"greetings": "",
                        "rephrase": False,
                        "notsure": False,
                        "notsure_search": "",
                        "gmaps": "",
                        "wikipedia": ""}

    if request.method == 'POST':
        user_input = request.get_json().get('query')
        print("L'utilisateur demande: '{}'".format(user_input))
        analysis = parser.Analyze(user_input)

        # take action depending on the parsing results. Whether calling Wikipedia or/and Google Maps API
        api_call = {1: wikipedia.Wikipedia,
                    2: gmaps.Gmaps}

        # action on greetings words
        if analysis.found_greetings:
            analysis_results.update({"greetings": analysis.found_greetings})

        # search  on location found
        if analysis.found_locations:
            maps_search = api_call[2](analysis.locations[0])
            wikipedia_search = api_call[1](analysis.locations[0])

            analysis_results.update({"gmaps": maps_search.response,
                                     "wikipedia": wikipedia_search.infos})

        # take a bet and search for the first entity found in input on Wikipedia
        else:
            if len(analysis.entities) != 0:
                wikipedia_search = api_call[1](analysis.entities[0].text)

                analysis_results.update({"wikipedia": wikipedia_search.infos,
                                         "notsure": True,
                                         "notsure_search": analysis.entities[0].text})

        # what to do if the parser don't understand the input
        if len(analysis.entities) == 0:
            analysis_results.update({"rephrase": True})

        print(analysis_results)

    return analysis_results

