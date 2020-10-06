import os
from flask import Flask, render_template, flash, redirect, session, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Tool
from dotenv import load_dotenv
from forms import UserRegistrationForm, UserLoginForm, ToolAddForm, ToolEditForm, UserEditForm
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

MAPQUEST_KEY = os.environ.get('MAPQUEST_CONSUMER_KEY')
BASE_URL = "http://www.mapquestapi.com/geocoding/v1"

connect_db(app)


# GET LAT AND LNG FOR USER BASED ON ADDRESS/ZIP/ETC
def get_map_center(address):
    center = [38.8159, 76.7497]

    res = requests.get(f"{BASE_URL}/address", params={'key': MAPQUEST_KEY, 'location': address})
    if res:
        data = res.json()
        lat = data["results"][0]['locations'][0]['latLng']['lat']
        lng = data["results"][0]['locations'][0]['latLng']['lng']
        center = [lat, lng]

    return center

# GET TOOL COORDS
def get_tool_coords(tools):

    zips = set([tool.location_id for tool in tools])

    locations = ""
    for z in zips:
        locations += f"&location={z},USA" #only works for USA currently, need to update model to be more dynamic
    

    res = requests.get(f"{BASE_URL}/batch?key={MAPQUEST_KEY}{locations}")
    print("*********response**********")
    print(res.status_code)
    print("*********KEY**********")
    print(MAPQUEST_KEY)
    print("*********locations**********")
    print(locations)
    data = res.json()

    postal_code_lat_long_map = {}
    for result in data["results"]:
        for location in result["locations"]:
            postal_code_lat_long_map[int(location["postalCode"])] = [
                location['latLng']['lat'], location['latLng']['lng']]

    """addressPoints = [
        list(postal_code_lat_long_map.get(tool.location_id)).append(tool.name)
        for tool in tools
    ]"""
    addressPoints = []

    for tool in tools:
        new_point = list.copy(postal_code_lat_long_map.get(tool.location_id))
        new_point.append(tool.name)
        new_point.append(tool.id)
        addressPoints.append(new_point)

    return addressPoints

# HOME PAGE ROUTE
@app.route('/')
def get_home():
    """Home Page"""
    if "username" not in session:
        return render_template('home.html')
    else:
        tools = Tool.query.all()
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        zip_code = user.zip_code
        center = get_map_center(zip_code)
        addresses = get_tool_coords(tools)

        return render_template('map.html', tools=tools, KEY=MAPQUEST_KEY, center=center, addresses=addresses)

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

# LOGOUT USER
@app.route('/logout')
def logout_user():
    session.pop("username")
    flash("Logged Out", "warning")
    return redirect('/')

# USER PROFILE PAGE
@app.route('/users/<username>')
def get_user_information(username):
    if "username" not in session:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')

    prof_user = User.query.filter_by(username=username).first()
    curr_username = session["username"]
    curr_user = User.query.filter_by(username=curr_username).first()
    return render_template('users/profile.html', prof_user=prof_user, curr_user=curr_user)

# EDIT YOUR USER
@app.route('/users/<username>/update', methods=["GET", "POST"])
def edit_user(username):
    user = User.query.filter_by(username=username).first()
    form = UserEditForm(obj=user)
    if "username" not in session:
        flash("please login first", "warning")
        return redirect('/login')
    
    if user.username != session["username"]:
        flash("Access Denied, please sign into the appropriate account", "danger")
        return redirect('/')

    if form.validate_on_submit():
        user.name = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.first_name = form.first_name.data 
        user.last_name = form.last_name.data 
        user.zip_code = form.zip_code.data
        user.img_url = form.img_url.data
        db.session.commit()
        flash("Account Updated!", "primary")
        return redirect(f"/users/{username}")
    
    return render_template('users/edit_user.html', form=form, username=session["username"])

# DELETE YOUR USER
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete the user"""
    if "username" not in session:
        flash("please login first", "warning")
        return redirect('/login')
    if username == session["username"]:
        curr_username = session["username"]
        curr_user = User.query.filter_by(username=curr_username).first()
        print("***********************")
        print(curr_user)
        db.session.delete(curr_user)
        db.session.commit()
        flash("DELETED USER", "success")
        session.pop("username")
        return redirect("/")
    flash("You don't have permission to delete that", "danger")
    return redirect('/')

# ADD A TOOL FORM
@app.route('/tools/add', methods=['GET', 'POST'])
def add_tool_form():
    """add a tool"""
    form = ToolAddForm()
    username = session["username"]
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
@app.route('/tools/<toolID>')
def get_tool_information(toolID):
    if "username" not in session:
        flash("You are not authorized to view that page", "danger")
        return redirect('/')
    
    tool = Tool.query.filter_by(id=toolID).first()
    return render_template('tools/tool_details.html', tool=tool)

# EDIT TOOL
@app.route('/tools/<toolID>/update', methods=["GET", "POST"])
def edit_tool(toolID):
    tool = Tool.query.get_or_404(toolID)
    form = ToolEditForm(obj=tool)
    if "username" not in session:
        flash("please login first", "warning")
        return redirect('/login')
    
    if tool.owner.username != session["username"]:
        flash("That is not your post", "danger")
        return redirect('/')

    if form.validate_on_submit():
        tool.name = form.name.data
        tool.description = form.description.data
        tool.available = form.available.data
        db.session.commit()
        flash("Tool Updated!", "primary")
        return redirect(f"/tools/{tool.id}")
    
    return render_template('tools/edit_tool.html', form=form, username=session["username"])

# DELETE TOOLS
@app.route('/tools/<toolID>/delete', methods=['POST'])
def delete_tool(toolID):
    """Delete the tool"""
    if "username" not in session:
        flash("please login first", "warning")
        return redirect('/login')
    tool = Tool.query.get_or_404(toolID)
    if tool.owner.username == session["username"]:
        db.session.delete(tool)
        db.session.commit()
        flash("DELETED", "success")
        return redirect(f"/users/{tool.owner.username}")
    flash("You don't have permission to delete that", "danger")
    return redirect('/')
