import os
from flask import Flask, render_template, flash, redirect, session, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Tool
from dotenv import load_dotenv
from forms import UserRegistrationForm, UserLoginForm, ToolAddForm
from sqlalchemy.exc import IntegrityError
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import localtime, strftime

app = Flask(__name__)

# dotenv config
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

# Add socketio to the app
socketio = SocketIO(app)
if __name__ == '__main__':
    socketio.run(app)
ROOMS = ["tool1", "tool2", "tool3", "tool4"]

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

    res = requests.get(f"{BASE_URL}/address", params={'key': MAPQUEST_KEY, 'location': address})

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
        new_point[2].replace("'", '"')
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
        print("****************************")
        print(addresses)

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

# Logout User
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

# DELETE TOOLS
@app.route('/users/<username>/tools/<toolID>/delete', methods=['POST'])
def delete_tool(username, toolID):
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



# ******************
# CHAT FEATURES HERE
# ******************

# GET CHAT PAGE
@app.route('/chat')
def chat_messages():
    username = session["username"]
    chats = ROOMS
    return render_template('chat.html', username=username, chats=chats)

@socketio.on('message')
def message(data):
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])

@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room "}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room "}, room=data['room'])