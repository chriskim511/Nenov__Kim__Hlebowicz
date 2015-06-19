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

def addGuide (title, url, userwhoposted, classtitle):
    if (checkGuide(title, url, userwhoposted, classtitle) == False):
        return False
    else:
        newGuide = {"title": title,"url": url, "userwhoposted":userwhoposted, "classtitle":classtitle}
        guides.insert(newGuide)
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
    result = guides.find({'classtitle': classtitle})
    guideList = []
    for guide in result:
        miniGuideList = []
        miniGuideList.append(guide['title'])
        miniGuideList.append(guide['url'])
        miniGuideList.append(guide['userwhoposted'])
        guideList.append(miniGuideList)
    return guideList  
