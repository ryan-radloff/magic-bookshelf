from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, RegisterForm, BookForm
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
#from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from os.path import join, dirname

# TODO: figure out whats wrong with python-dotenv because it returns every string with quotes
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
Base = declarative_base()
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap(app)

Session = sessionmaker()
# Sqlalchamy database
# TODO: Change the SQL database when done
s = "mysql+mysqlconnector://{username}:{password}@{server}/bookshelf_db".format(username = "root", password = os.getenv('PASSWORD'), server = "104.197.168.142:3306")
engine = create_engine(s)
engine.connect()


Session.configure(bind=engine)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{server}/bookshelf_db".format(username = "root", password = "p@xs8Ddz4.YVT-QweUZE", server = "104.197.168.142:3306")
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

# Login 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).filter(User.user_id == user_id).first()


##CREATE TABLE IN DB
class User(UserMixin, Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(250))
    username = Column(String(25), unique=True)
    password = Column(String(1000))
    is_authenticated = True

    def get_id(self):
        return (self.user_id)

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    isbn = Column(Integer)
    owner = Column(Integer)
# Below required once, when creating DB. 
# db.create_all()


@app.route('/')
def index():
    # Todo: index should know if a user is logged in or not
    # and conditionally render clickables
    # print(User.query.get(1))
    return render_template('index.html')


@app.route('/create_listing', methods=["GET", "POST"])
@login_required
def create_listing():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(isbn=int(form.isbn.data),
                        owner=current_user.user_id)
        session = Session()
        session.add(new_book)
        session.commit()

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
        session = Session()
        if session.query(User).filter(User.email==form.email.data).first():
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

        session.add(new_user)
        session.commit()
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
        session = Session()
        # User from database
        new_user = session.query(User).filter(User.email==email).first()

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

@app.route('/book_list', methods=["GET", "POST"])
def listings():
    session = Session()
    return render_template('book_list.html', query=session.query(Book))

@app.route('/<string:name>/listing', methods=["GET", "POST"])
def listing(name):
    session = Session()
    return render_template('book_info.html', book=session.query(Book).filter(Book.book_id==name).first())

if __name__ == "__main__":
    app.run(debug=True)
