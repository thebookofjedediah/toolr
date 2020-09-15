import os
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv

app = Flask(__name__)

# dotenv config
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', 'secret_backup')
# Redirects are not blocked here - set this next line to True or delet it in order to enable them
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# HOME PAGE ROUTE
@app.route('/')
def get_home():
    """Home Page"""
    return render_template('home.html')