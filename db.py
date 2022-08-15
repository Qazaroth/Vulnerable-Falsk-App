from main import DB_FILENAME
from User import User

import shelve

def setupDB():
    usersDict = {}
    try:
        db = shelve.open(DB_FILENAME, "r")
        usersDict = db["Users"]
    except:
        db = shelve.open(DB_FILENAME, "c")
        u = User("Admin", "admin", 0)
        usersDict[u.getID] = u
        db["Users"] = usersDict
    finally:
        User.countId = len(usersDict)
        db.close()

def getAccountByID(id) -> User:
    try:
        db = shelve.open(DB_FILENAME, "r")
        usersDict = db["Users"]
        db.close()

        for key in usersDict:
            v : User = usersDict[key]

            if v.getID() == id:
                return v
    except:
        return None

    return None

def getAccountsByUsername(username):
    accs = []
    try:
        db = shelve.open(DB_FILENAME, "r")
        usersDict = db["Users"]
        db.close()

        for key in usersDict:
            v : User = usersDict[key]

            if v.getUsername() == username:
                accs.append(v)
    except:
        return None

    return accs

def checkIfAccExists(id):
    db = shelve.open(DB_FILENAME, "r")
    usersDict = db["Users"]
    db.close()

    for key in usersDict:
        if key == id:
            return True

    return False

def getAllAccounts():
    accs = []

    db = shelve.open(DB_FILENAME, "r")
    usersDict = db["Users"]
    db.close()

    for k in usersDict:
        accs.append(usersDict[k])

    return accs