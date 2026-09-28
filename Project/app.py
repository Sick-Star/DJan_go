#!/home/codespace/.python/current/bin/python3
from flask import Flask, redirect, url_for, render_template, request, session
import sqlalchemy

app = Flask(__name__)
app.secret_key = "nosferatu" #setting up a key to protect data stored in the session

@app.route("/login", methods=["POST", "GET"])
def login():
    #determine whether a request is POST or GET
    if request.method == "POST": 
        session.permanent = True #seting the permanent session
        user_input = request.form["nm"] #we are passing the name input from login.html file using the name we gave it 'nm'
        session["username"] = user_input #storing value inside 'user_input' (from previous line) in the session key "username"

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
            email = request.form["email"] #we are grapping the email from user.html
            session["Email"] = email #making a session with a session key 'Email'
        else:
            if "Email" in session:
                email = session["Email"]

        return render_template("user.html", mail=email)
    else:
        return redirect(url_for("login")) # retun this only if the session key "username" is not inside the session
    

if __name__ == "__main__":
    app.run(debug=True)
