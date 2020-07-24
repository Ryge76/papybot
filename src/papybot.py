from flask import render_template, request, jsonify, Blueprint

from .config import FE_GMAPS_KEY
from .utils import make_decision


bp = Blueprint("papybot", __name__)


@bp.route("/index/")
@bp.route("/")
def index():
    """Root view function"""
    return render_template("index.html", key=FE_GMAPS_KEY)


@bp.route("/search/", methods=["POST"])
def search():
    """Search logic for user's input"""
    if request.method == "POST":
        user_input = request.get_json().get("query")

        print("L'utilisateur demande: '{}'".format(user_input))

        analysis = make_decision(user_input)

        print(analysis)

    return jsonify(analysis)
