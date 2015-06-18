import pymongo, hashlib
from pymongo import MongoClient
client = MongoClient()

db = client.database

users = db.users
guides = db.guides
classes = db.classes

#return true if valid input; false if not
def checkPassword(passwordToCheck):
    return len(passwordToCheck) > 0

def checkUsername(usernameToCheck):
    return ((len(usernameToCheck) > 0) and (users.find({"username":usernameToCheck}).count()==0))

def checkPost(postToCheck):
    return len(postToCheck) > 0

def addUser(username, password):
    record = users.find({"username":username})
    if ((checkUsername(username) == False) or (checkPassword(password) == False)):
        return False
    else:
        newUser = {"username": username,"password": hashlib.sha512(password).hexdigest()}
        users.insert(newUser)
        return True

def validateUser(username, password):
    record = users.find({"username":username})
    if (record.count() != 1):
        return False
    else:
        return record[0]['password'] == hashlib.sha512(password).hexdigest()




