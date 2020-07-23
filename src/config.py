import os

base = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')
GMAPS_KEY = os.environ.get('GMAPS_KEY')
FLASK_APP = os.environ.get('FLASK_APP')
FLASK_ENV = os.environ.get('FLASK_ENV')