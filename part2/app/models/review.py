import re
from place import Place
from user import User

from app.models.base import BaseModel

class Review(BaseModel):
    """Model class representing a review"""
    
    def __init__(self, text, rating, place, user):
        """Initialize the review with provided details"""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
    
    @property
    def text(self):
        """Get the review text"""
        return self.__text
    
    @text.setter
    def text(self, value):
        """Set the review text"""
        if not value:
            raise ValueError("Review text cannot be empty")
        self.__text = value
    
    @property
    def rating(self):
        """Get the rating of the review"""
        return self.__rating
    
    @rating.setter
    def rating(self, value):
        """Set the rating of the review"""
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value
    
    @property
    def place(self):
        """Get the place being reviewed"""
        return self.__place
    
    @place.setter
    def place(self, value):
        """Set the place being reviewed"""
        if not isinstance(value, Place):
            raise ValueError("Invalid place instance")
        self.__place = value
    
    @property
    def user(self):
        """Get the user who wrote the review"""
        return self.__user
    
    @user.setter
    def user(self, value):
        """Set the user who wrote the review"""
        if not isinstance(value, User):
            raise ValueError("Invalid user instance")
        if not value:
            raise ValueError("User cannot be empty")
        self.__user = value