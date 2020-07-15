from flask import render_template, request, jsonify

from .config import GMAPS_KEY
from . import create_app
from .utils import make_decision

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

        analysis = make_decision(user_input)

        print(analysis)

    return jsonify(analysis)

