from flask import Flask, render_template, request, session
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

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if validLogin(request.form['username'],
                      request.form['password']):
            return login(request.form['username'])

    return render_template('login.html', error=error)

@app.route('/studyguides',methods=['GET','POST'])
def guides():
    return render_template('classes.html')

@app.route('/studyguides/<classname>')
def showClassGuides():
    return render_template('classguides.html',classname=classname)

if __name__ == '__main__':
    app.run(debug=True)
