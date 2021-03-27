from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, RegisterForm, BookForm
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Sqlalchamy database
# TODO: Change the SQL database when done
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))

    def get_id(self):
           return (self.user_id)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    owner = db.Column(db.String(100))

# Below required once, when creating DB. 
# db.create_all()

@app.route('/')
def index():
    # Todo: index should know if a user is logged in or not
    # and conditionally render clickables
    # print(User.query.get(1))
    return render_template('index.html')


@app.route('/create-listing', methods=["GET", "POST"])
@login_required
def create_listing():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title = request.form.get("Title"),
                        isbn = request.form.get("ISBN"),
                        author=request.form.get("Author"),
                        owner= current_user.username)
        
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("data"))
    # Very important, make sure to initialize the field of the OWNER's
    # associated user's ID after the post request. To be handled later
    return render_template('create_listing.html', form=form)

# def post_listing():


@app.route('/data/', methods=['POST', 'GET'], strict_slashes=False)
# apparently strict_slashes=False is required here if debug=True...
@login_required
def data():
    if request.method == 'GET':
        return "Can't access directly! Post through /create-listing"
    if request.method == 'POST':
        form_data = request.form
        return render_template('submitted_data.html', form_data=form_data)


@app.route('/register', methods=["GET", "POST"])
def register():

    # TODO: If user is already Loggedin
    if current_user.is_authenticated == True:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            #User already exists
            msg = "User with this email already exist, log in instead!"
            return redirect(url_for('login'))

        hashed_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=10
        )
        new_user = User(
            email=form.email.data,
            username=form.username.data,
            password=hashed_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("index"))

    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():

    # DO not login in if alredy logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    msg = ""
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # User from database
        new_user = User.query.filter_by(email=email).first()

        # Wrong email
        if (not new_user) or (not check_password_hash(new_user.password, password)): 
            msg = "Wrong Username or Password"
            return render_template('login.html', form=form, msg = msg)
        else:
            login_user(new_user)
            return redirect(url_for("index"))
    return render_template('login.html', form=form, msg = msg)


@app.route("/<string:name>/profile")
def show_profile(name):
    return render_template('profile.html', name=name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
