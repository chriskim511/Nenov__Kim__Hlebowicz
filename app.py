from flask import Flask, session, flash, redirect, render_template, request, url_for
import database
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
app = Flask(__name__)
app.secret_key = 'lmao' 

@app.route('/home')
def home():
    if 'username' in session:
        return render_template("maindisplay.html", user = session['username'])
    else:
        flash("You are not logged in")
        return redirect(url_for('login'))

@app.route('/', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if(database.validateUser(username,password) == False):
            error = 'Unregistered username or incorrect password'
            return redirect(url_for('login'))
        flash("You've logged in successfully")
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route('/addc', methods=["GET","POST"])
def addc():
    if request.method == "POST":
        classtitle = request.form["classname"]
        teachername = request.form["teachername"]
        subject = request.form["subject"]
        database.addClass(classtitle,teachername,subject)
    return render_template("subjectdisplay.html",classes=database.getClasses(subject), subject=subject)

@app.route('/addg', methods=["GET","POST"])
def addg():
    classtitle = request.form["classtitle"]
    title = request.form["title"]
    userwhoposted = session['username']
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    database.addGuide(title,'/uploads/'+filename,userwhoposted,classtitle)
    return render_template("classdisplay.html",guides=database.getGuides(classtitle), classtitle=classtitle)

@app.route('/subject/<subject>/', methods=["GET","POST"])
def subject(subject):
    return render_template("subjectdisplay.html",classes=database.getClasses(subject), subject=subject)

@app.route('/class/<classtitle>/')
def classtitle(classtitle):
    return render_template("classdisplay.html",guides=database.getGuides(classtitle), classtitle=classtitle)


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



app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'odt', 'ppt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)
