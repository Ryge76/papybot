from flask import render_template, request
from .config import GMAPS_KEY
from . import create_app

app = create_app()


@app.route('/')
def index():
    if request.method == 'POST':
        return render_template('index.html', key=GMAPS_KEY)
    else:
        return render_template('index.html', key=GMAPS_KEY)


@app.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':

        return render_template('index.html', key=GMAPS_KEY)
    else:
        return render_template('index.html')

