from flask import render_template, url_for
from .config import GMAPS_KEY
from . import create_app

app = create_app()


@app.route('/')
def index():
    return render_template('index.html', key=GMAPS_KEY)

@app.route('/search/', methods=['POST'])
def search():
    return "On line !"

