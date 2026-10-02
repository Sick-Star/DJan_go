#!/mnt/c/Users/dilet/OneDrive/Documents/Amazon_project/DJan_go/Project/.venv/bin/python3
from flask import Flask, redirect, url_for, render_template, request, session
from sqlalchemy.util.preloaded import import_prefix
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "nosferatu" #setting up a key to protect data stored in the session

#############################################################################################################
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3' #config to where SQLAlchemy should store your database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #error handling for sqlalchemy turned off
#############################################################################################################

app.permanent_session_lifetime = timedelta(minutes=5)

##################################################################################################################
db = SQLAlchemy(app) #creates a SQLAlchemy database object and connects it to your Flask app
##################################################################################################################

class users(db.Model): #making a class named users
    _id = db.Column("ID", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email
####################################################################################################################

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    #determine whether a request is POST or GET
    if request.method == "POST": 
        session.permanent = True #seting the permanent session
        user_input = request.form["nm"] #we are passing the name input from login.html file using the name we gave it 'nm'
        session["username"] = user_input #storing value inside 'user_input' (from previous line) in the session key "username"

        found_user = users.query.filter_by(name=user_input).first() #doing a query search using the username entered by the user
        if found_user:
            session["Email"] = found_user.email #storing the email we get back from the database in a session
        else:
            usr = users(user_input, None) #sending username back to class and email set to None
            db.session.add(usr) #adds it to database
            db.session.commit() #save by committing it
        return redirect(url_for("user")) #redirects us to /user
    
    else:
        if "username" in session:
            return redirect(url_for("user")) #if we are already logged in and headed /login we are directed to the user page
        
        return render_template("login.html") #if user is not logged in it takes you to the login page

@app.route("/logout")
def logout():
    session.pop("username", None) #delete the session key "username" and return none after loging out
    session.pop("Email", None) #delete the session key 'Email' after logging out
    return redirect(url_for("login")) #if they they visit logout delete the session and redirect them back to the login page

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "username" in session: #is there a session key "username" in the session
        user = session["username"] # get session key "username" and store it in user

        if request.method == "POST":
            email = request.form["mail"] #we are grapping the email entered from user.html 'mail' is the name
            session["Email"] = email #making a session with a session key 'Email'
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email #everytime the user makes a Post email request we update the database with it.
            db.session.commit() #make sure to commit and save your changes
        else:
            if "Email" in session:
                email = session["Email"]

        return render_template("user.html", mail=email)
    else:
        return redirect(url_for("login")) # return this only if the session key "username" is not inside the session
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
