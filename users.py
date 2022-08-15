from flask import Blueprint, jsonify, session, request, render_template, redirect, url_for
from User import User
from main import DB_FILENAME

import re
import shelve

bp = Blueprint("users", __name__)

def checkAllAccountsLogin(username, password) -> User:
    accs = []

    db = shelve.open(DB_FILENAME, "r")
    usersDict = db["Users"]
    db.close()

    for key in usersDict:
        value = usersDict[key]
        if value.getUsername() == username:
            if value.isCorrectPassword(password):
                accs.append(value)

    if len(accs) > 0:
        return accs[0]
    
    return None

def checkAllAccountsRegister(username) -> User:
    accs = []

    db = shelve.open(DB_FILENAME, "r")
    usersDict = db["Users"]
    db.close()

    for key in usersDict:
        value = usersDict[key]
        if value.getUsername() == username:
            accs.append(value)

    if len(accs) > 0:
        return accs[0]
    
    return None


@bp.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        acc : User = checkAllAccountsLogin(username, password)

        if acc is not None:
            session["loggedIn"] = True
            session["ID"] = acc.getID()
            session["access"] = acc.getAccessLevel()
            session["Username"] = acc.getUsername()

            return redirect(url_for("main.home"))
        else:
            msg = "Incorrect username and/or password!"
    
    return render_template("user/login.html", msg=msg, title="MOU Bank - Login")

@bp.route("/logout")
def logout():
    session.pop("loggedIn", None)
    session.pop("ID", None)
    session.pop("access", None)
    session.pop("Username", None)

    return redirect(url_for("main.home"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]

        acc = checkAllAccountsRegister(username)

        if acc is not None:
            msg = "Account already exists!"
        elif not username or not password:
            msg = "Please fill out the form!"
        else:
            u = User(username, password)

            db = shelve.open(DB_FILENAME, "w")
            usersDict = db["Users"]
            usersDict[u.getID()] = u
            db["Users"] = usersDict
            db.close() 

            return redirect(url_for("users.login"))
    
    return render_template("user/register.html", msg=msg, title="MOU Bank - Register")