import os
from flask import Flask, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from dotenv import load_dotenv
from forms import UserRegistrationForm, UserLoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# dotenv config
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///tool-share')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'secret_backup')
# Redirects are not blocked here - set this next line to True or delet it in order to enable them
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# HOME PAGE ROUTE
@app.route('/')
def get_home():
    """Home Page"""
    return render_template('home.html')

# USER REGISTRATION
@app.route('/register', methods=['GET', 'POST'])
def user_registration():
    """User Registration Page"""
    form = UserRegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        zip_code = form.zip_code.data

        new_user = User.register(username, password, email, first_name, last_name, zip_code)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username is taken")
            return render_template('users/register.html', form=form)
       
        flash(f"Welcome {first_name}, we successfully created your account!", "success")
        return redirect('/')
    else:
        return render_template('users/register.html', form=form)

# LOG IN AS USER
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}", "success")
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('users/login.html', form=form)