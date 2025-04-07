import re
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.base import BaseModel
#-----------------------------------place_amenities join table-----------------------------------
place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

#-----------------------------------Place Table model-----------------------------------

class Place(BaseModel):
    """Model class representing a place"""
    __tablename__ = 'places'

    _title = db.Column(db.String(100), nullable=False)
    _description = db.Column(db.String(500), nullable=False)
    _price = db.Column(db.Float, nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    _owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    _reviews = db.relationship('Review', backref='place', lazy=True)
    _amenities = db.relationship('Amenity', secondary=place_amenities, backref='places', lazy=True)

#-----------------------------------title.getter-----------------------------------
    
    @hybrid_property
    def title(self):
        """Get the title of the place"""
        return self._title
    
#-----------------------------------title.setter-----------------------------------

    @title.setter
    def title(self, value):
        """Set the title of the place"""
        if not value:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title cannot be longer than 100 characters")
        self._title = value
    
#-----------------------------------description.getter-----------------------------------

    @hybrid_property
    def description(self):
        """Get the description of the place"""
        return self._description
    
#-----------------------------------description.setter-----------------------------------

    @description.setter
    def description(self, value):
        """Set the description of the place"""
        if not value:
            raise ValueError("Description cannot be empty")
        self._description = value
    
#-----------------------------------price.getter-----------------------------------

    @hybrid_property
    def price(self):
        """Get the price of the place"""
        return self._price
    
#-----------------------------------price.setter-----------------------------------

    @price.setter
    def price(self, value):
        """Set the price of the place"""
        if not isinstance (value, (int, float)) or value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
    
#-----------------------------------latitude.getter-----------------------------------
    @hybrid_property
    def latitude(self):
        """Get the latitude of the place"""
        return self._latitude
    
#-----------------------------------latitude.setter-----------------------------------

    @latitude.setter
    def latitude(self, value):
        """Set the latitude of the place"""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value
    
#-----------------------------------longitude.getter-----------------------------------

    @hybrid_property
    def longitude(self):
        """Get the longitude of the place"""
        return self._longitude
    
#-----------------------------------longitude.setter-----------------------------------
    
    @longitude.setter
    def longitude(self, value):
        """Set the longitude of the place"""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value
    
#-----------------------------------owner_id.getter-----------------------------------

    @hybrid_property
    def owner_id(self):
        """Get the owner of the place"""
        return self._owner_id
    
#-----------------------------------owner_id.setter-----------------------------------

    @owner_id.setter
    def owner(self, value):
        """Set the owner of the place"""
        if not value:
            raise ValueError("Owner cannot be empty")
        self._owner_id = value

#-----------------------------------amenities.getter-----------------------------------

    @hybrid_property 
    def amenities(self):
        return self._amenities
    
#-----------------------------------amenities.setter-----------------------------------

    @amenities.setter
    def amenities(self, value):
        if not isinstance(value, list):
            raise ValueError("Amenities must be a list")
        self._amenities = value
