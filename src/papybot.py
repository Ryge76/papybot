from flask import render_template, request, jsonify

from .config import GMAPS_KEY
from . import create_app
from .utils import make_decision

app = create_app()


@app.route('/index/')
@app.route('/')
def index():
    
    return render_template('index.html', key=GMAPS_KEY)


@app.route('/search/', methods=['POST'])
def search():

    if request.method == 'POST':
        user_input = request.get_json().get('query')

        print("L'utilisateur demande: '{}'".format(user_input))

        analysis = make_decision(user_input)

        print(analysis)

    return jsonify(analysis)

