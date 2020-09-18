import os
from flask import Flask, render_template, flash, redirect, session
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
    if "user_id" not in session:
        return render_template('home.html')
    else:
        return render_template('map.html')

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

        session["user_id"] = new_user.id # Keeps user logged in
        session["username"] = user.username # Keeps user logged in
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
            session["user_id"] = user.id # Keeps user logged in
            session["username"] = user.username # Keeps user logged in
            flash(f"Welcome back, {user.username}", "success")
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('users/login.html', form=form)

# Logout User
@app.route('/logout')
def logout_user():
    session.pop("user_id")
    session.pop("username")
    flash("Logged Out", "warning")
    return redirect('/')

# USER PROFILE PAGE
@app.route('/users/<username>')
def get_user_information(username):
    if "username" not in session or username != session['username']:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')
    user_id = session["user_id"]
    user = User.query.get(user_id)
    return render_template('users/profile.html', user=user)

# ADD A TOOL FORM
@app.route('/username/tools/add', methods=['GET', 'POST'])
def add_tool_form(username):
    form = ToolAddForm()

    if "username" not in session or username != session['username']:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_tool = Tool() #*************Add the form code here
        db.session.add(new_tool)
        db.session.commit()
        flash("New Tool Added", "success")
        return redirect(f"/users/{username}")

    user_id = session["user_id"]
    user = User.query.get(user_id)
    return render_template('add_tool.html', user=user, form=form)