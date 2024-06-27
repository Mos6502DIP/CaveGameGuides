import sqlite3
from flask import Flask, send_file, request, Response, redirect, render_template
App = Flask(__name__)
import json
import hashlib


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


@App.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = hash_string(str(request.form['Password']))
        login = McLogin(Username, Password)
        if login:
            response = "Login Successful"
        else:
            response = "Login Failed"

        return render_template("login.html", response=response)

    else:
        return render_template("login.html")


@App.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        Username = request.form['Username']
        Email = request.form['Email']
        Password = hash_string(str(request.form['Password']))
        register = CreateAccount(Email, Username, Password)
        if register:
            response = "Account Creation Successful"
        else:
            response = "Account Creation Failed"
        return render_template("register.html", response=response)
    else:
        return render_template("register.html")


@App.route('/courses', methods=['GET', 'POST'])
def Courses():
    info = load_json("course_info")
    return render_template("courses.html", info=info)


if __name__ == '__main__':
    App.run( host='0.0.0.0', port=8080, debug=True)
