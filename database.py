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

def checkClass(classnameToCheck,teacherToCheck):
    return ((len(classnameToCheck)) > 0) and ((len(teacherToCheck)) > 0) and (classes.find({"classname":classnameToCheck}).count()==0)

def checkGuide(titleToCheck, urlToCheck, userwhopostedToCheck, classtitleToCheck):
    return (len(titleToCheck) > 0) and (len(urlToCheck) > 0) and (len(userwhopostedToCheck) > 0) and (len(classtitleToCheck) > 0) and (guides.find({"title":titleToCheck,"url":urlToCheck, "userwhoposted":userwhopostedToCheck,"classtitle":classtitleToCheck}).count()==0)

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

def addClass (classname, teacher, subject):
    if (checkClass(classname, teacher) == False):
        return False
    else:
        newClass = {"classname": classname,"teacher": teacher,"subject": subject}
        classes.insert(newClass)
        return True

def addGuide (title, url, votes, userwhoposted, classtitle):
    if (checkGuide(title, url, userwhoposted) == False):
        return False
    else:
        newClass = {"classname": classname,"teacher": teacher}
        classes.insert(newClass)
        return True

def getClasses(subject):
    result = classes.find({'subject': subject})
    classList = []
    for post in result:
        miniClassList = []
        miniClassList.append(post['classname'])
        miniClassList.append(post['teacher'])
        classList.append(miniClassList)
    return classList

def getGuides(classtitle):
    result = classes.find({'classname': classtitle})
    classList = []
    for post in result:
        miniClassList = []
        miniClassList.append(post['classname'])
        miniClassList.append(post['teacher'])
        classList.append(miniClassList)
    return classList  

addClass('AP Econ', 'Schweitz', 'Social Studies')
addClass('AP Econ', 'Schweitz', 'Social Studies')
addClass('AP Math', 'Schweitz', 'Math')
addClass('AP Math 2', 'Aviggy', 'Math')
addClass('AP Math 2', 'Ye', 'History')







