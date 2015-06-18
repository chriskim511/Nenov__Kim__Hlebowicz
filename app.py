from flask import Flask,render_template, session, redirect, request, url_for, g, flash
from functools import wraps
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "key"

client = MongoClient()
db = client['studyData']
accountDB = db['accounts']
guideDB = db['guides']

def validate_email(email):
    at = str.find(email, "@")
    period = str.find(email, ".")
    if (at <= 0) or (period <= 0) or (at >= len(email)-5) or (period >= len(email) - 3):
        return False
    else:
        return True

def upper(password):
    uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for p in password:
        if (str.find(uppers, p) >= 0):
            return True
    return False

def lower(password):
    lowers = "abcdefghijklmnopqrstuvwxyz"
    for p in password:
        if (str.find(lowers, p) >= 0):
            return True
    return False

def digit(password):
    digits = "1234567890"
    for p in password:
        if (str.find(digits, p) >= 0):
            return True
    return False
def validate_password(password):
    return (len(password) >= 5) and (len(password) <= 21) and (upper(password)) and (lower(password)) and (digit(password))


@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():

        if request.method=="GET":
                #print urlopen(abc).read()
                return render_template("login.html")
                #print response
        else:
                #print response
                username = request.form["username"]
                password = request.form["password"]
                button = request.form["b"]
                if button == "Login":
                    user = users.find_one({'username': username})
                    if user == None:
                        flash("Not a Valid Username")
                        return redirect(url_for('login'))
                    elif user['password'] != password:
                        flash("Password and username do not match")
                        return redirect(url_for('login'))
                    else:
                            #flash("Welcome to Leaf")
                        session['username'] = username
                        session['password'] = password
                        session['gender'] = user['gender']
                        session['emailaddress'] = user['emailaddress']
                        session['month'] = user['month']
                        session['day'] = user['day']
                        session['year'] = user['year']
                        print ratedschools
                        if username not in ratedschools:
                            ratedschools['%s' % username] = []
                        if user['first'] == 0:
                            return redirect(url_for('profile'))
                        return redirect(url_for('user_home', username=username))
                #flash("Welcome to leaf")
				#flash("Welcome to Leaf")
				#return redirect(url_for('user_home', username=username))
		else: 
                    return redirect(url_for('register'))
def add_user(username, password, emailaddress, gender, month, day, year) : #, age
    user = {'username' : username, 
                        'password' : password,
                        'emailaddress' : emailaddress,
                        'gender' : gender,
                        'month' : month,
                        'day' : day,
                        'year' : year,
                        'first' : 0,
                        #'age' : age
                        }
    return users.insert(user)
@app.route("/register",methods=["GET","POST"])
def register():
	if request.method=="GET":
                m = []
                for x in range(1,13):
                    m.append(x)
                d = []
                for x in range(1,32):
                    d.append(x)
                y = []
                for x in range(97,1,-1):
                    y.append(x + 1919)
                return render_template("register.html", m=m, d=d, y=y)
	else: 
        	button = request.form["b"]
		if button == "Login":
        	        return redirect(url_for('login'))
         	username = request.form["username"]
        	password = request.form["password"]
		password2 = request.form["password2"]
		gender = request.form["gender"]
                month = request.form["month"]
                day = request.form["day"]
                year = request.form["year"]
        	emailaddress = request.form["emailaddress"]
		if users.find_one({'username': username}) != None:
			flash("The username you submitted is already taken, please try again.")
			return redirect(url_for('register'))
		if users.find_one({'emailaddress': emailaddress}) != None:
			flash("The email you submitted already has an account tied to it, please try again.")
			return redirect(url_for('register'))
		if not validate_email(str(emailaddress)):
			flash("This is not an email")
			return redirect(url_for('register'))
		if not password == password2:
			flash("Passwords do not match")
			return redirect(url_for('register'))
		if not validate_password(str(password)):
			flash("The password does not meet the above requirements.")
			return redirect(url_for('register'))
		add_user(username, password, emailaddress, gender, month, day, year) #, age
		flash("You've sucessfully registered, now login!")
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
    	session.pop('username', None)
    	session.pop('password', None)
    	session.pop('first_name', None)
    	session.pop('last_name', None)
	flash("You have successfully logged out")
    	return redirect(url_for('login'))

@app.route("/home/<username>",methods=["GET","POST"])
def user_home(username=None):
    if request.method == "GET":
        session['username'] = username
        #print session['username']
        session.modified=True
        return render_template("home.html", username=username)
    else:
        if 'b' in request.form:
            button = request.form["b"]
    	    if button=="Logout":
                    return redirect(url_for("logout"))
        value = request.form['q']
        #print "this is the value"
        #print value
        return redirect(url_for("search",field=value))


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


        
