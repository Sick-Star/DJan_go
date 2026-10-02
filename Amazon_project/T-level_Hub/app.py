#!/mnt/c/Users/dilet/OneDrive/Documents/Amazon_project/DJan_go/Project/.venv/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Amazon"

#Database configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3' #config to where SQLAlchemy should store your database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #error handling for sqlalchemy turned off

app.permanent_session_lifetime = timedelta(days=5) #setting up permanent session

#Connecting your app with your database
db = SQLAlchemy(app) #creates a SQLAlchemy database object and connects it to your Flask app

#Database calss
class users(db.Model): #making a class named users
    _id = db.Column("ID", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    age = db.Column(db.String(20))

    def __init__(self, username, password, email=None, age=None):
        self.username = username
        self.password = password
        self.email = email
        self.age = age


@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["Uname"].lower().strip()
        user_passwd = request.form["Passwd"].strip()

        #creating a session
        session["Username"] = user_name
        session["Password"] = user_passwd

        found_user = users.query.filter_by(username=user_name).first()

        if found_user != None: #checks that the username entered is in database
            if user_passwd == found_user.password :
                return redirect(url_for("profile"))
        else:
            flash("Username not found! Please sign up to continue.")
            return redirect(url_for("signup"))
    else:
        return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        user_name = request.form["uname"].lower().strip()
        user_passwd = request.form["passwd"].strip()

        #creating a session
        session["Username"] = user_name
        session["Password"] = user_passwd

        found_user = users.query.filter_by(username=user_name).first()
        if found_user != None:
            if found_user.username.lower() == user_name.lower(): #found_user and allows us to return 'None' if no user is found
                flash("Username already exists. Try logging in")
                return redirect(url_for("login"))
        else:
            usr = users(username=user_name, password=user_passwd)
            db.session.add(usr)
            db.session.commit()
            flash("User created. Try logging in to your new account.")
            return redirect(url_for("login"))
    else:
        return render_template("signup.html")


@app.route("/resource")
def resource():
    return render_template("resource.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/discussion")
def discussion():
    return render_template("discussion.html")

@app.route("/admin")
def admin():
        return render_template("view.html", values=users.query.all())

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/profile", methods=["POST", "GET"])
def profile():
    if request.method == "POST":
        email = request.form["mail"].lower().strip()
        date_of_birth = request.form["age"]

        session["Email"] = email
        session["Birth_Date"] = date_of_birth


        found_user = users.query.filter_by(username=session["Username"]).first()
        if found_user == None:
            return redirect(url_for("login"))

        else:
            found_user.email = email
            found_user.age = date_of_birth
            db.session.commit()
            flash("Changes to profile complete. please try logging in again to see changes.")
            return redirect(url_for("login"))

    else:
        found_user = users.query.filter_by(username=session["Username"]).first()
        if "Email" in session and "Birth_Date" in session:
            return render_template("userInfo.html", username=session["Username"], password=session["Password"], email=found_user.email, age=found_user.age)

        return render_template("userInfo.html", username=session["Username"], password=session["Password"])

if __name__ == "__main__":

    with app.app_context():
        # db.drop_all()  #deletes your whole database
        db.create_all()
    app.run(debug=True)

