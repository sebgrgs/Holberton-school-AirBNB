import re

from app.models.base import BaseModel


class User(BaseModel):
    """Model class representing a user"""
    def __init__(self, email, first_name, last_name, is_admin=False):
        """Initialize the user with provided details"""
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    @property
    def first_name(self):
        """Get the first name of the user"""
        return self.__first_name
    
    @first_name.setter
    def first_name(self, value):
        """Set the first name of the user"""
        if not value:
            raise ValueError("First name cannot be empty")
        if len(value) > 50:
            raise ValueError("First name cannot be longer than 50 characters")
        self.__first_name = value
    
    @property
    def last_name(self):
        """Get the last name of the user"""
        return self.__last_name
    
    @last_name.setter
    def last_name(self, value):
        """Set the last name of the user"""
        if not value:
            raise ValueError("Last name cannot be empty")
        if len(value) > 50:
            raise ValueError("Last name cannot be longer than 50 characters")
        self.__last_name = value
    
    @property
    def email(self):
        """Get the email of the user"""
        return self.__email
    
    @email.setter
    def email(self, value):
        """Set the email of the user"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            raise ValueError("Invalid email address")
        self.__email = value

    @property
    def is_admin(self):
        """Get the admin status of the user"""
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Set the admin status of the user"""
        if not isinstance(value, bool):
            raise ValueError("Admin status must be a boolean")
        self.__is_admin = value