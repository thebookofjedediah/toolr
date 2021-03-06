from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired

class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    zip_code = IntegerField("Zip Code", validators=[InputRequired()])

class UserEditForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    zip_code = IntegerField("Zip Code", validators=[InputRequired()])
    img_url = StringField("Image URL")

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class ToolAddForm(FlaskForm):
    name = StringField("Tool Name", validators=[InputRequired()])
    description = TextAreaField("Tool Description", validators=[InputRequired()])

class ToolEditForm(FlaskForm):
    name = StringField("Tool Name", validators=[InputRequired()])
    description = TextAreaField("Tool Description", validators=[InputRequired()])
    available = BooleanField("Available?")