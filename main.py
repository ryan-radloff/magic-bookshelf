from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.route('/')
def index():
    # Todo: index should know if a user is logged in or not
    # and conditionally render clickables
    return render_template('index.html')


@app.route('/create-listing')
def create_listing():
    return render_template('create_listing.html')


@app.route('/data/', methods=['POST', 'GET'], strict_slashes=False)
# apparently strict_slashes=False is required here if debug=True...
def data():
    if request.method == 'GET':
        return "Can't access directly! Post through /create-listing"
    if request.method == 'POST':
        form_data = request.form
        return render_template('submitted_data.html', form_data=form_data)


@app.route("/<string:name>/profile")
def show_profile(name):
    return render_template('profile.html', name=name)


if __name__ == "__main__":
    app.run(debug=True)
