import re

from app.models.base import BaseModel

class Amenity(BaseModel):
    """Model class representing an amenity"""
    
    def __init__(self, id, name):
        """Initialize the amenity with provided details"""
        super().__init__()
        self.name = name
    
    @property
    def name(self):
        """Get the name of the amenity"""
        return self.__name
    
    @name.setter
    def name(self, value):
        """Set the name of the amenity"""
        if not value:
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name cannot be longer than 50 characters")
        self.__name = value