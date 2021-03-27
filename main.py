from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/<string:name>/profile")
def show_profile(name):
    return render_template('profile.html', name=name)


if __name__ == "__main__":
    app.run(debug=True)
