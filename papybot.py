from flask import render_template
from .config import GMAPS_KEY
from . import create_app

app = create_app()


@app.route('/')
def index():
    return render_template('index.html', key=GMAPS_KEY)

