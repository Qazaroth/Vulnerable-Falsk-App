from datetime import datetime

from flask import render_template, url_for, session, redirect, request
from User import User
from main import createApp, DB_FILENAME

import db

app = createApp()

def hasNoEmptyParams(rule):
    default = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()

    return len(default) >= len(arguments)

@app.before_first_request
def beforeFirstRequest():
    db.setupDB()

@app.after_request
def addCSPHeaders(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Security-Policy"] = "script-src 'self' 'unsafe-inline'"
    return response

@app.route("/sitemap", methods=["GET"])
def sitemap():
    links = []
    users = db.getAllAccounts()

    isLoggedIn = session.get("loggedIn")
    if isLoggedIn == True:
        id = session["ID"]
        user : User = db.getAccountByID(id)

        for rule in app.url_map.iter_rules():
            if ("GET" in rule.methods or "POST" in rule.methods) and hasNoEmptyParams(rule):
                if not "static" in rule.endpoint:
                    url = url_for(rule.endpoint, **(rule.defaults or {}))
                    links.append((url, rule.endpoint, ','.join(rule.methods)))

        return render_template("sitemap.html", urls=links)

    return redirect(url_for("main.home"))