import uuid
from datetime import datetime


class BaseModel:
    """Base model class that provides common attributes and methods"""
    def __init__(self):
        """Initialize the base model with a unique ID and timestamps"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attrib of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
