import sqlite3
from flask import *

import json
import hashlib
import random
import string
from emailpy import emails as ep
from datetime import timedelta

App = Flask(__name__)
App.secret_key = "lucario"
App.permanent_session_lifetime = timedelta(minutes=30)

def email_password():

    try:
        with open("email_password.txt") as fp:
            lines = fp.readlines()
            for line in lines:
                if line.strip()[0] != "#":
                    setting_line = line.strip().split("=")
                    if setting_line[0] == "password":
                        return setting_line[1]

    except FileNotFoundError:
        print("File not found")
        return None

comfirm = {}


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


def hash_string(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_json(file):
    with open(file + ".json", 'r') as f:
        data = json.load(f)
    return data

def CreateAccount(Email, Username, Password):
    Con = sqlite3.connect("Database.db")
    Cur = Con.cursor()
    Data = Cur.execute("SELECT * FROM Users WHERE Email = ? OR Username = ?", (Email, Username)).fetchall()


    if len(Data) == 0:
        Cur.execute("INSERT INTO Users(Email, Username, Password) VALUES (?, ?, ?)", (Email, Username, Password))
        print("Account Creation Successful")
        Con.commit()
        return True
    else:
        print("Account Creation Attempt Made: Error - Already Exists")
        return False


def check(Email, Username, Password):
    Con = sqlite3.connect("Database.db")
    Cur = Con.cursor()
    Data = Cur.execute("SELECT * FROM Users WHERE Email = ? OR Username = ?", (Email, Username)).fetchall()

    if len(Data) == 0:
        return True
    else:
        print("Account Creation Attempt Made: Error - Already Exists")
        return False


def McLogin(Username, Password):
    Con = sqlite3.connect("Database.db")
    Cur = Con.cursor()
    DbPass = Cur.execute("SELECT Password FROM Users WHERE Username = ?", (Username,)).fetchone()[0]

    if (len(DbPass) == 0):


        print("Account Login Attempt Made: Error - Does Not Exist")
        return False
    else:
        if DbPass == Password:
            print("Successful Login")
            return True
        else:
            print("Account Login Attempt Made: Error - Does Not Exist")
            return False

def get_username():
    if "Username" in session:
        return session["Username"]
    else:
        return "None"


def get_courses(username):
    print(username)
    info = load_json("course_info")
    user_course = ["Redstone Trap", "Ender Pearl Stasis Chamber",  "Tree Farm", "Automatic Fish Farm"]
    usr_re = {}
    for item in info["Java"]:
        if item in user_course:
            usr_re[item] = info["Java"][item]

    return usr_re




@App.route('/', methods=['GET', 'POST'])
def Landing():
    username = get_username()
    return render_template("home.html", username=username)


@App.route('/login/', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = hash_string(str(request.form['Password']))
        login = McLogin(Username, Password)
        if login:
            response = "Login Successful"
            session.permanent = True
            session["Username"] = Username

            return redirect("/dashboard")
        else:
            response = "Login Failed"

            username = get_username()
            return render_template("login.html", response=response, Username=username)

    else:
        username = get_username()
        return render_template("login.html", username=username)


@App.route('/register/', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':


        Username = request.form['Username']
        Email = request.form['Email']
        Password = hash_string(str(request.form['Password']))
        register = check(Email, Username, Password)
        if register:
            ComfirmId = get_random_string(10)

            comfirm[ComfirmId] = {}
            comfirm[ComfirmId]["Username"] = Username
            comfirm[ComfirmId]["Email"] = Email
            comfirm[ComfirmId]["Password"] = Password
            sender_email = 'telepy.noreply@gmail.com'
            sender_password = email_password()  # Please request the file which contain the password.
            recipient_email = Email
            subject = 'Redstone Zone Email verification'
            message = f"http://127.0.0.1:5000/verify/{ComfirmId}"
            ep.send_email(sender_email, sender_password, recipient_email, subject, message)
            response = "Please verify your email address (We have sent you a confirmation email)"
            username = get_username()
        else:
            response = "Account Creation Failed"
            username = get_username()
        return render_template("register.html", response=response, username=username)
    else:
        username = get_username()
        return render_template("register.html" , username=username)


@App.route('/verify/<code>/', methods=['GET', 'POST'])
def verify(code):
        if code in comfirm.keys():
            username = comfirm[code]["Username"]
            Email = comfirm[code]["Email"]
            Password = comfirm[code]["Password"]
            if CreateAccount(Email, username, Password):
                return render_template("verify.html")
            else:
                response = "Account Creation Failed"
                username = get_username()
                return render_template("register.html", response=response, username=username)

        else:
            response = "Account Creation Failed"
            username = get_username()
            return render_template("register.html", response=response, username=username)




@App.route('/courses/', methods=['GET', 'POST'])
def Courses():
    info = load_json("course_info")
    username = get_username()
    return render_template("courses.html", info=info, username=username)

@App.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if get_username() is not "None":
        return render_template("dashboard.html", username=get_username(),  info=get_courses(get_username()))

    else:
        return redirect("/login")


@App.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    username = get_username()
    response = "Logout Successful"
    return redirect("/")





if __name__ == '__main__':
    App.run( host='0.0.0.0', port=5000, debug=True)
