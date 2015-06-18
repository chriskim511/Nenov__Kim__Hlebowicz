from flask import Flask,render_template, session, redirect, request, url_for, g, flash
from functools import wraps

app = Flask(_name_)
app.secret_key = "key"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("guides", methods=["GET","POST"])
def guides():
    return render_template("guides.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")


        
