from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from .config import GMAPS_KEY

app = Flask(__name__)
app.config.from_object('papybot.config')

Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html', key=GMAPS_KEY)

