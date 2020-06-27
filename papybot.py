from flask import render_template, request, make_response, jsonify
from .config import GMAPS_KEY
from . import create_app

from .components.lang import parser
from .components.api import maps
from .components.api import wikipedia

app = create_app()


@app.route('/')
def index():
    
    return render_template('index.html', key=GMAPS_KEY)


@app.route('/search/', methods=['POST'])
def search():

    analysis_results = {"greetings": False,
                        "greeting_word": "",
                        "rephrase": False,
                        "notsure": False,
                        "notsure_search": "",
                        "searched_word": "",
                        "gmaps": "",
                        "wikipedia": ""}

    if request.method == 'POST':
        user_input = request.get_json().get('query')
        print("L'utilisateur demande: '{}'".format(user_input))
        analysis = parser.Analyze(user_input)

        # take action depending on the parsing results. Whether calling
        # Wikipedia or/and Google Maps API
        api_call = {1: wikipedia.Wikipedia,
                    2: maps.Gmaps}

        # action on greetings words
        if analysis.found_greetings:
            analysis_results.update({"greeting_word":
                                     analysis.greetings[0]})

        # search  on location found
        if analysis.found_locations:
            maps_search = api_call[2]().get(analysis.locations[0])
            wikipedia_search = api_call[1](analysis.locations[0])

            analysis_results.update({"gmaps": maps_search,
                                     "wikipedia": wikipedia_search.infos,
                                     "searched_word": analysis.locations[0]})

        # take a bet and search for the first entity found in input on Wikipedia
        else:
            if len(analysis.entities) != 0:
                wikipedia_search = api_call[1](analysis.entities[0].text)
                maps_search = api_call[2]().get(analysis.entities[0].text)

                analysis_results.update({"wikipedia": wikipedia_search.infos,
                                         "notsure": True,
                                         "notsure_search": analysis.entities[0].text,
                                         "gmaps": maps_search})

        # what to do if the parser don't understand the input
        if len(analysis.entities) == 0:
            analysis_results.update({"rephrase": True})

        print(analysis_results)
        # response = make_response(analysis_results)
        # response.headers.update({'Content-type': 'application/json'})

    return jsonify(analysis_results)

