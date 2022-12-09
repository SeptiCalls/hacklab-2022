from datetime import datetime
from csv import DictReader, DictWriter, QUOTE_NONNUMERIC
from flask import Flask, render_template, session, url_for, request, redirect


db = open("static/users.csv", 'a')
reader = DictReader(db)
writer = DictWriter(db, fieldnames=["username","name","email","password"])


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "q7vytnycnv3y7nc87y8wedssw4ytv5beyv748sytvn74vynt"


title = "scrap dealings"

def checkCookie(u_name):
    with open("static/user.csv", 'r') as db:
        reader = DictReader(db)
        for row in reader:
            if u_name == row["username"]:
                return True
    return False



def isValid(u_name, p_word):
    with open("static/user.csv", 'r') as db:
        reader = DictReader(db)
        for row in reader:
            if u_name == row["username"] and p_word == row["password"]:
                return True
    return False


def addUser(u_name, e_mail, p_word):
    with open("static/user.csv", 'a') as db:
        writer = DictWriter(db, fieldnames=["username", "email", "password"])
        writer.writerow({"username": u_name, "email": e_mail, "password": p_word}, QUOTE_NONNUMERIC)


@app.route("/")
@app.route("/home")
def index():

    if not session.get("username"):
        return redirect("/login")

    return render_template("index.html", title=title, user=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if isValid(username, password):
            session["username"] = username
            return render_template('index.html', title=title, user=username)
        
        return render_template("login.html", error="Invalid Password")

    if request.method == "GET":
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # conf_pass = request.forms.get("conf_pass")
        addUser(username, email, password)
        session["username"] = username
        return render_template("index.html", title=title, user=username)

    if request.method == "GET":
        if checkCookie(session.get("username")):
            return render_template("login.html")
        else:
            return render_template("register.html")


@app.route("/logout")
def logout():
    session["username"] = None
    return render_template("index.html", title=title, user=None)


if __name__ == "__main__":
    app.run(debug=True)