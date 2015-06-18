from flask import Flask, session, flash, redirect, render_template, request, url_for
import database
app = Flask(__name__)
app.secret_key = 'lmao' 

def login(username):
    session['username'] = username
    return

#def validLogin(user,password):
    #Check database to see if user exists

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/login', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if(database.validateUser(username,password) == False):
            error = 'Unregistered username or incorrect password'
            return redirect(url_for('home'))
        flash("You've logged in successfully")
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/signup', methods=["GET","POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not database.addUser(username,password):
            flash("Registered username, too short username, or too short password.")
            return redirect(url_for('signup'))
        flash("Great! You've registered! Now you can log in.")
        return redirect(url_for('login'))
    return render_template("signup.html")


@app.route('/studyguides',methods=['GET','POST'])
def guides():
    return render_template('classes.html')

@app.route('/studyguides/<classname>')
def showClassGuides():
    return render_template('classguides.html',classname=classname)

if __name__ == '__main__':
    app.run(debug=True)
