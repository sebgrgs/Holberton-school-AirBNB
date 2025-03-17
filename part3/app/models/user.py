import re
from app.models.base import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
from app import db

bcrypt = Bcrypt()
#-----------------------------------User Table Model-----------------------------------
class User(BaseModel):
    """Model class representing a user"""
    __tablename__ = 'users'

    _first_name = db.Column(db.String(50), nullable=False)
    _last_name = db.Column(db.String(50), nullable=False)
    _email = db.Column(db.String(120), nullable=False, unique=True)
    _password = db.Column(db.String(128), nullable=False)
    _is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

#-----------------------------------function to hash password-----------------------------------

    def hash_password(self, password):
        """Hash the password using bcrypt"""
        return bcrypt.generate_password_hash(password).decode('utf-8')

#-----------------------------------function to verify password hashing-----------------------------------

    def verify_password(self, password):
        """Verify the password using bcrypt"""
        return bcrypt.check_password_hash(self._password, password)

#-----------------------------------first_name.getter-----------------------------------

    @hybrid_property
    def first_name(self):
        """Get the first name of the user"""
        return self._first_name

#-----------------------------------first_name.setter-----------------------------------

    @first_name.setter
    def first_name(self, value):
        """Set the first name of the user"""
        if not value:
            raise ValueError("First name cannot be empty")
        if len(value) > 50:
            raise ValueError("First name cannot be longer than 50 characters")
        self._first_name = value

#-----------------------------------last_name.getter-----------------------------------

    @hybrid_property
    def last_name(self):
        """Get the last name of the user"""
        return self._last_name

#-----------------------------------last_name.setter-----------------------------------
    
    @last_name.setter
    def last_name(self, value):
        """Set the last name of the user"""
        if not value:
            raise ValueError("Last name cannot be empty")
        if len(value) > 50:
            raise ValueError("Last name cannot be longer than 50 characters")
        self._last_name = value

#-----------------------------------email.getter-----------------------------------
    
    @hybrid_property
    def email(self):
        """Get the email of the user"""
        return self._email

#-----------------------------------email.setter-----------------------------------
    
    @email.setter
    def email(self, value):
        """Set the email of the user"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            raise ValueError("Invalid email address")
        self._email = value

#-----------------------------------is_admin.getter-----------------------------------

    @hybrid_property
    def is_admin(self):
        """Get the admin status of the user"""
        return self._is_admin
    
#-----------------------------------is_admin.setter-----------------------------------

    @is_admin.setter
    def is_admin(self, value):
        """Set the admin status of the user"""
        if not isinstance(value, bool):
            raise ValueError("Admin status must be a boolean")
        self._is_admin = value

#-----------------------------------password.getter-----------------------------------

    @hybrid_property
    def password(self):
        """Get the hashed password of the user"""
        return self._password

#-----------------------------------password.setter-----------------------------------

    @password.setter
    def password(self, value):
        """Set the password of the user"""
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value) < 6:
            raise ValueError("Password cannot be shorter than 6 characters")
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')
