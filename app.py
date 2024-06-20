from flask import Flask, send_file, request, Response, redirect, render_template
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']

        return render_template("home.html", response="Null")
    else:
        return render_template(f"home.html", response="Null")


if __name__ == '__main__':
    app.run()
