from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm, RegisterForm, BookForm, ChangePasswordForm, RequestForm
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from os.path import join, dirname

# TODO: figure out whats wrong with python-dotenv because it returns every string with quotes
# dotenv_path = join(dirname(__file__), '.env')
load_dotenv()
app = Flask(__name__)
Base = declarative_base()
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap(app)

Session = sessionmaker()
# # Sqlalchamy database
# # TODO: Change the SQL database when done
s = "mysql+mysqlconnector://{username}:{password}@{server}/bookshelf_db".format(username = "root", password = os.getenv('PASSWORD'), server = "104.197.168.142:3306")
engine = create_engine(s)
engine.connect()
Session.configure(bind=engine)



# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{server}/bookshelf_db".format(username = "root", password = "p@xs8Ddz4.YVT-QweUZE", server = "104.197.168.142:3306")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

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
    credits = Column(Integer)
    totalcredit = Column(Integer)
    is_authenticated = True

    def get_id(self):
        return (self.user_id)

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    isbn = Column(Integer)
    owner = Column(Integer, ForeignKey('users.user_id'))
# Below required once, when creating DB. 
# db.create_all()

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    address_to = Column(String(100))
    address_from = Column(String(100))
    complete = Column(Boolean)
    seller = Column(Integer, ForeignKey('users.user_id'))
    buyer = Column(Integer, ForeignKey('users.user_id'))
    book = Column(Integer, ForeignKey('books.book_id'))


@app.route('/', methods = ["GET", "POST"])
def index():
    # Todo: index should know if a user is logged in or not
    # and conditionally render clickables
    # print(User.query.get(1))
    return render_template('index.html', user=current_user, msg=request.args.get('msg'))


@app.route('/create_listing', methods=["GET", "POST"])
@login_required
def create_listing():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(
            isbn=int(form.isbn.data),
            owner=current_user.user_id
        )

        session = Session()
        session.add(new_book)
        session.commit()
        
        new_transaction = Transaction(
            seller=current_user.user_id,
            book=new_book.book_id,
            address_from=form.streetNameNum.data + " " + form.city.data + ", " + form.state.data + " " + form.zipcode.data
        )

        session.add(new_transaction)
        session.commit()

        return redirect(url_for("index", msg="The Magic Bookshelf📚 applauds your generosity! You have earned [✨Arcane Dust x1]"))
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
            credits=0,
            totalcredit=0
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
@login_required
def show_profile(name):

    # DO not login in if alredy logged in
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
        
    session = Session()
    ob=session.query(Book).filter(Book.owner == current_user.user_id)
    return render_template('profile.html', current_user=current_user, owned_books=ob)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    session = Session()
    if form.validate_on_submit():
        hashed_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=10
        )
        # Test the below line of code
        user = session.query(User).filter(User.user_id==current_user.user_id).first()
        user.password = hashed_salted_password
        session.commit()
        return redirect(url_for("index"))
    return render_template("change_password.html", form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/book_list', methods=["GET", "POST"])
def listings():
    session = Session()
    return render_template('book_list.html', query=session.query(Book))

@app.route('/<string:id>/listing', methods=["GET", "POST"])
def listing(id):
    session = Session()
    return render_template('book_info.html', book=session.query(Book).filter(Book.book_id==id).first())

@app.route('/request_book/<string:id>', methods=["GET", "POST"])
@login_required
def request_book(id):
    session = Session()
    trans = session.query(Transaction).filter(Transaction.book==id).first()
    if (trans.address_to):
        return redirect(url_for("listings"))
    form = RequestForm()
    if form.validate_on_submit():
        
        
        trans.address_to = form.streetNameNum.data + " " + form.city.data + ", " + form.state.data + " " + form.zipcode.data
        trans.buyer = current_user.user_id

        session.commit()

        return redirect(url_for("listings"))
    # Very important, make sure to initialize the field of the OWNER's
    # associated user's ID after the post request. To be handled later
    return render_template('request_book.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
