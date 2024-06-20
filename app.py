import sqlite3
from flask import Flask, send_file, request, Response, redirect, render_template
App = Flask(__name__)


con = sqlite3.connect("Database.db")




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
