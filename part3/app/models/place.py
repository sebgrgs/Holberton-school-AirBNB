import re

from app.models.base import BaseModel


class Place(BaseModel):
    """Model class representing a place"""
    
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        """Initialize the place with provided details"""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = amenities or []
    
    @property
    def title(self):
        """Get the title of the place"""
        return self.__title
    
    @title.setter
    def title(self, value):
        """Set the title of the place"""
        if not value:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title cannot be longer than 100 characters")
        self.__title = value
    
    @property
    def description(self):
        """Get the description of the place"""
        return self.__description
    
    @description.setter
    def description(self, value):
        """Set the description of the place"""
        if not value:
            raise ValueError("Description cannot be empty")
        self.__description = value
    
    @property
    def price(self):
        """Get the price of the place"""
        return self.__price
    
    @price.setter
    def price(self, value):
        """Set the price of the place"""
        if not isinstance (value, (int, float)) or value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value
    
    @property
    def latitude(self):
        """Get the latitude of the place"""
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        """Set the latitude of the place"""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self.__latitude = value
    
    @property
    def longitude(self):
        """Get the longitude of the place"""
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        """Set the longitude of the place"""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self.__longitude = value
    
    @property
    def owner(self):
        """Get the owner of the place"""
        return self.__owner
    
    @owner.setter
    def owner(self, value):
        """Set the owner of the place"""
        if not value:
            raise ValueError("Owner cannot be empty")
        self.__owner = value

    @property 
    def amenities(self):
        return self.__amenities
        
    @amenities.setter
    def amenities(self, value):
        if not isinstance(value, list):
            raise ValueError("Amenities must be a list")
        self.__amenities = value
