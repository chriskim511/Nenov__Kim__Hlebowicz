from flask import Flask,render_template, session, redirect, request, url_for, g, flash
from functools import wraps
from pymongo import MongoClient

app = Flask(_name_)
app.secret_key = "key"

client = MongoClient()
db = client['studyData']
accountDB = db['accounts']
guideDB = db['guides']


@app.route("/")
def home():
    return render_template("index.html")

@app.route("guides", methods=["GET","POST"])
def guides():
    return render_template("guides.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/login")
def login():
    return render_template("login.html")


        
