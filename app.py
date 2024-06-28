import sqlite3
from flask import Flask, send_file, request, Response, redirect, render_template
App = Flask(__name__)
import json
import hashlib
import random
import string
from emailpy import emails as ep

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


@App.route('/', methods=['GET', 'POST'])
def Landing():
    return render_template("home.html")


@App.route('/login/', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = hash_string(str(request.form['Password']))
        login = McLogin(Username, Password)
        if login:
            response = "Login Successful"
        else:
            response = "Login Failed"

        return render_template("login.html", response=response[])

    else:
        return render_template("login.html")


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
        else:
            response = "Account Creation Failed"
        return render_template("register.html", response=response)
    else:
        return render_template("register.html")


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
                return render_template("register.html", response=response)

        else:
            response = "Account Creation Failed"
            return render_template("register.html", response=response)




@App.route('/courses/', methods=['GET', 'POST'])
def Courses():
    info = load_json("course_info")
    return render_template("courses.html", info=info)


if __name__ == '__main__':
    App.run( host='0.0.0.0', port=8080, debug=True)
