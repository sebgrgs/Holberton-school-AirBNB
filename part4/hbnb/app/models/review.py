from app.models.base import BaseModel
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
import re

#-----------------------------------Review Table Model-----------------------------------

class Review(BaseModel):
    """Model class representing a review"""
    """Initialize the review with provided details"""
    __tablename__ = 'reviews'
        
    _text = db.Column(db.String(500), nullable=False)
    _rating = db.Column(db.Integer, nullable=False)
    _place_id = db.Column(db.String(100), db.ForeignKey('places.id'), nullable=False)
    _user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)

#-----------------------------------text.getter-----------------------------------
    
    @hybrid_property
    def text(self):
        """Get the review text"""
        return self._text

#-----------------------------------text.setter-----------------------------------

    @text.setter
    def text(self, value):
        """Set the review text"""
        if not value:
            raise ValueError("Review text cannot be empty")
        self._text = value

#-----------------------------------rating.getter-----------------------------------
    
    @hybrid_property
    def rating(self):
        """Get the rating of the review"""
        return self._rating

#-----------------------------------rating.setter-----------------------------------
    
    @rating.setter
    def rating(self, value):
        """Set the rating of the review"""
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

#-----------------------------------place_id.getter-----------------------------------
    
    @hybrid_property
    def place_id(self):
        """Get the place ID being reviewed"""
        return self._place_id

#-----------------------------------place_id.setter-----------------------------------
    
    @place_id.setter
    def place_id(self, value):
        """Set the place ID being reviewed"""
        if not isinstance(value, str):
            raise ValueError("Place ID must be a string")
        self._place_id = value

#-----------------------------------user_id.getter-----------------------------------
    
    @hybrid_property
    def user_id(self):
        """Get the user ID who wrote the review"""
        return self._user_id

#-----------------------------------user_id.setter-----------------------------------
    
    @user_id.setter
    def user_id(self, value):
        """Set the user ID who wrote the review"""
        if not isinstance(value, str):
            raise ValueError("User ID must be a string")
        self._user_id = value