from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

# *********************
# Begin Classes/Models Here
# *********************

# User Model
class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.Text, default="/static/images/default-pic.png")

    tools = db.relationship("Tool", backref="owner", cascade="all,delete")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name, zip_code):
        """Register a user with hashed password and return the user"""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn into unicode
        hashed_utf8 = hashed.decode("utf8")

        # return the user with hashed password
        return cls(username=username,
            password=hashed_utf8, 
            email=email, 
            first_name=first_name, 
            last_name=last_name,
            zip_code=zip_code)

    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that a user exists and password is correct
        Return user if valid; else return false"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


# Tools Model
class Tool(db.Model):
    """Tools model"""

    __tablename__ = 'tools'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    owner_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        nullable=False)

    # renter_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('users.id'))

    name = db.Column(db.String(50), nullable=False)

    description = db.Column(db.Text, nullable=False)

    img_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png")

    location_id = db.Column(
        db.Integer,
        nullable=False)

    available = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # owner = db.relationship('User', backref="tools", foreign_keys=[owner_id])
 
# Message Model
# class Message(db.Model):
#     """Message model"""

#     __tablename__ = 'messages'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     writer_name = db.Column(
#         db.String, 
#         db.ForeignKey('users.username'),
#         nullable=False)

#     content = db.Column(db.Text, nullable=False)

#     time = db.Column(
#         db.String,
#         nullable=False,
#         default=datetime.utcnow())

#     writer = db.relationship('User', backref="message", foreign_keys=[writer_name])