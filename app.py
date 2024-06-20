import sqlite3
from flask import Flask, send_file, request, Response, redirect, render_template
App = Flask(__name__)


Con = sqlite3.connect("Database.db")
Cur = Con.cursor()

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


@App.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        Username = request.form['Username']
        Email = hash(request.form['Email'])
        Password = hash(request.form['Password'])

    return render_template("register.html")


if __name__ == '__main__':
    App.run()
