from pathlib import Path
from flask import Flask
from User import User

import shelve

DB_FILENAME = "database.db"

def createApp():
    app = Flask(__name__)
    app.secret_key = "abcdefghijklmnopqrstuvwxyz"

    db_path = Path(DB_FILENAME)
    if db_path.exists():
        db_path.unlink()

    usersDict = {}
    try:
        db = shelve.open(DB_FILENAME, "r")
        usersDict = db["Users"]
    except:
        db = shelve.open(DB_FILENAME, "c")

        admin = User("admin", "admin", 0)
        usersDict[admin.getID()] = admin

        db["Users"] = usersDict
    finally:
        User.countId = len(usersDict)
        db.close()

    with app.app_context():
        import users
        import index
        import admins

        app.register_blueprint(index.bp)
        app.register_blueprint(users.bp)
        app.register_blueprint(admins.bp)

        return app