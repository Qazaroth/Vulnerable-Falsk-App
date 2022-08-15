from flask import Blueprint, jsonify, session, request, render_template
from main import DB_FILENAME

import shelve

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    msg = ""

    isLoggedIn = session.get("loggedIn")
    if isLoggedIn == True:
        username = session["Username"]
        msg = username

    return render_template("index.webfile", msg=msg, title="Vulnerable Falsk App")
