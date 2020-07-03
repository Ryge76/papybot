import os

base = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')
GMAPS_KEY = os.environ.get('GMAPS_KEY')
