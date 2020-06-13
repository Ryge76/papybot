from flask import render_template, request
from .config import GMAPS_KEY
from . import create_app

app = create_app()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', key=GMAPS_KEY)
    else:
        return render_template('index.html', key=GMAPS_KEY)


