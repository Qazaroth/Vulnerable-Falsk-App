import base64

class User:
    countId = -1
    def __init__(self, username, password, accessLvl=1) -> None:
        self.__id = User.countId + 1
        self.__username = username
        self.__password = base64.b64encode(str.encode(password))
        self.__accessLvl = accessLvl
        User.countId += 1

    def getID(self):
        return self.__id

    def setUsername(self, username):
        self.__username = username

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def setPassword(self, password):
        self.__password = base64.b64encode(str.encode(password))

    def isCorrectPassword(self, password):
        return self.__password == base64.b64encode(str.encode(password))

    def setAccessLevel(self, accessLvl):
        self.__accessLvl = accessLvl
        
    def getAccessLevel(self):
        return self.__accessLvl