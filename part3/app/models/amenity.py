import re
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.base import BaseModel
from app.models.place import place_amenities

class Amenity(BaseModel):
    
    """Initialize the amenity with provided details"""
    table_name = 'amenities'
    _name=db.Column(db.String(50), nullable=False)
    places = db.relationship('Place', secondary=place_amenities, backref='amenities', lazy=True)
    
    @hybrid_property
    def name(self):
        """Get the name of the amenity"""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set the name of the amenity"""
        if not value:
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name cannot be longer than 50 characters")
        self._name = value