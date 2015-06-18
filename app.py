from flask import Flask,render_template, session, redirect, request, url_for, g, flash
from functools import wraps
from pymongo import MongoClient

app = Flask(_name_)
app.secret_key = "key"

client = MongoClient()
db = client['studyData']
accountDB = db['accounts']
guideDB = db['guides']

def curUser():
    if loggedin(): 
        return session["username"]
    else: 
        return "Anon"

def loggedin():
    return "username" in session

def requirelogin(f):
    @wraps(f)
    def ff():
        if loggedin():
            return f()
        else:
            return redirect("/")
        return ff

@app.route("/")
def home():
    return render_template("index.html",sess = session)

@app.route("guides", methods=["GET","POST"])
def guides():
    guideList = guideDB.find()
    return render_template("guides.html",gList = guideList)

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/login")
def login():
    return render_template("login.html")


        
