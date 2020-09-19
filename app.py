import os
from flask import Flask, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Tool
from dotenv import load_dotenv
from forms import UserRegistrationForm, UserLoginForm, ToolAddForm
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
    if "username" not in session:
        return render_template('home.html')
    else:
        tools = Tool.query.all()
        return render_template('map.html', tools=tools)

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

        session["username"] = new_user.username # Keeps user logged in
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
            session["username"] = user.username # Keeps user logged in
            flash(f"Welcome back, {user.username}", "success")
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('users/login.html', form=form)

# Logout User
@app.route('/logout')
def logout_user():
    session.pop("username")
    flash("Logged Out", "warning")
    return redirect('/')

# USER PROFILE PAGE
@app.route('/users/<username>')
def get_user_information(username):
    if "username" not in session or username != session['username']:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')

    user = User.query.filter_by(username=username).first()
    return render_template('users/profile.html', user=user)

# ADD A TOOL FORM
@app.route('/users/<username>/tools/add', methods=['GET', 'POST'])
def add_tool_form(username):
    form = ToolAddForm()
    
    if "username" not in session or username != session['username']:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first() #get the user
        name = form.name.data
        description = form.description.data

        new_tool = Tool(owner_id=user.id, name=name, description=description, location_id=user.zip_code)
        db.session.add(new_tool)
        db.session.commit()
        flash("New Tool Added", "success")
        return redirect(f"/users/{username}")

    user = User.query.filter_by(username=username).first()
    return render_template('tools/add_tool.html', user=user, form=form)

# TOOL DETAILS PAGE
@app.route('/users/<username>/tools/<toolID>')
def get_tool_information(username, toolID):
    if "username" not in session:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')
        
    tool = Tool.query.filter_by(id=toolID).first()
    return render_template('tools/tool_details.html', tool=tool)