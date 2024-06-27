import sqlite3
from flask import Flask, send_file, request, Response, redirect, render_template
App = Flask(__name__)
import json


Con = sqlite3.connect("Database.db")
Cur = Con.cursor()

def load_json(file):
    with open(file + ".json", 'r') as f:
        data = json.load(f)
    return data

def CreateAccount(Email, Username, Password):
    Data = Cur.execute("SELECT * FROM Users WHERE Email = ? OR Username = ?", (Email, Username)).fetchall()
    

    if len(Data) == 0:
        Cur.execute("INSERT INTO Users(Email, Username, Password) VALUES (?, ?, ?)", (Email, Username, Password))
        print("Account Creation Successful")
        Con.commit()
        return True
    else:
        print("Account Creation Attempt Made: Error - Already Exists")
        return False
    

def Login(Email, Password):
    Data = Cur.execute("SELECT * FROM Users WHERE Email = ? AND Password = ?", (Email, Password)).fetchall()

    if (len(Data) == 0):
        print("Account Login Attempt Made: Error - Does Not Exist")
        return False
    else:
        print("Successful Login")
        return True


@App.route('/', methods=['GET', 'POST'])
def Landing():
    return render_template("home.html")


@App.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        Email = hash(request.form['Email'])
        Password = hash(request.form['Password'])

    return render_template("login.html")


@App.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        Username = request.form['Username']
        Email = hash(request.form['Email'])
        Password = hash(request.form['Password'])

    return render_template("register.html")

@App.route('/courses', methods=['GET', 'POST'])
def Courses():
    info = load_json("course_info")
    return render_template("courses.html", info=info)


if __name__ == '__main__':
    App.run( host='0.0.0.0', port=8080, debug=True)
