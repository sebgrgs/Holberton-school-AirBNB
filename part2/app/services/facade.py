from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, **user_data):
        """Update user in repository"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        updates = {}
        for field, value in user_data.items():
            if hasattr(user, field):
                updates[field] = value

        updated_user = self.user_repo.update(user_id, updates)

        if updated_user is None:
            updated_user = self.get_user(user_id)

        return updated_user
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity in repository"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        updates = {}
        for field, value in amenity_data.items():
            if hasattr(amenity, field):
                updates[field] = value

        updated_amenity = self.amenity_repo.update(amenity_id, updates)

        if updated_amenity is None:
            updated_amenity = self.get_amenity(amenity_id)

        return updated_amenity

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return

    def get_place(self, place_id):
        pass

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        pass