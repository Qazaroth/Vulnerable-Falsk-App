from flask import Blueprint, jsonify, session, request, render_template, redirect, url_for
from User import User
from main import DB_FILENAME

import db

bp = Blueprint("admins", __name__)

@bp.route("/admin/users", methods=["GET"])
def users():
    users = db.getAllAccounts()

    isLoggedIn = session.get("loggedIn")
    if isLoggedIn == True:
        id = session["ID"]
        user : User = db.getAccountByID(id)

        if user.getAccessLevel() == 0:
            return render_template("admins/users.html", title="ADMIN MOU Bank - Users", users=users)

    return redirect(url_for("main.home"))