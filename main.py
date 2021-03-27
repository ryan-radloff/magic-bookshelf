from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'



@app.route('/')
def index():
    return f"<h1>Magic Book Shelf</h1>"

@app.route('/login', methods=["GET", "POST"])
def login():
    return f"<h1>Magic Book Shelf</h1>"


if __name__ == "__main__":
    app.run(debug=True)
