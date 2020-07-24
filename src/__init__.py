import os
from flask import Flask


"""
Application factory.
"""


def create_app(test_config=None):
    """Create default application or application with custom configuration"""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY")
                                       or os.urandom(24))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import papybot

    app.register_blueprint(papybot.bp)

    return app
