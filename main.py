from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.route('/')
def index():
    return f"<h1>Magic Book Shelf</h1>"

@app.route('/login', methods=["GET", "POST"])
def login():
    return f"<h1>Magic Book Shelf - Login</h1>"

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return f"<h1>Magic Book Shel - SignUp</h1>"


@app.route("books/<int:id>/", methods=["GET", "POST"])
def book(id):
    return f"<h1>Good to Great - By Jim Collins</h1>"

if __name__ == "__main__":
    app.run(debug=True)
