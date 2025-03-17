from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository, UserRepository, AmenityRepository, PlaceRepository, ReviewRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app import db

#-----------------------------------HBnBFacade-----------------------------------

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

#-----------------------------------create_user-----------------------------------
    
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

#-----------------------------------get_user-----------------------------------

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

#-----------------------------------get_user_by_email-----------------------------------

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

#-----------------------------------get_all_users-----------------------------------

    def get_all_users(self):
        return self.user_repo.get_all()

#-----------------------------------update_user-----------------------------------

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

#-----------------------------------delete_user-----------------------------------
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

#-----------------------------------get_amenity-----------------------------------

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

#-----------------------------------get_all_amenities-----------------------------------

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

#-----------------------------------update_amenity-----------------------------------

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

#-----------------------------------delete_amenity-----------------------------------
    
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

#-----------------------------------create_place-----------------------------------

    def create_place(self, place_data):
        """Create new place"""
        amenity_ids = [amenity['id'] for amenity in place_data.pop('amenities', [])]
        amenities = db.session.query(Amenity).filter(Amenity.id.in_(amenity_ids)).all()
        
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=place_data['owner_id'],
            amenities=amenities
        )
        
        self.place_repo.add(place)
        return place

#-----------------------------------get_place-----------------------------------

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

#-----------------------------------get_all_places-----------------------------------

    def get_all_places(self):
        return self.place_repo.get_all()

#-----------------------------------update_place-----------------------------------

    def update_place(self, place_id, place_data):
        """Update place in repository"""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        updates = {}
        for field, value in place_data.items():
            if hasattr(place, field):
                updates[field] = value

        updated_place = self.place_repo.update(place_id, updates)

        if updated_place is None:
            updated_place = self.get_place(place_id)

        return updated_place

#-----------------------------------delete_place-----------------------------------
    
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

#-----------------------------------create_review-----------------------------------
    
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

#-----------------------------------get_review-----------------------------------

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

#-----------------------------------get_all_reviews-----------------------------------

    def get_all_reviews(self):
        return self.review_repo.get_all()
#-----------------------------------get_reviews_by_place-----------------------------------

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        reviews = []
        for review in self.review_repo.get_all():
            if review.place_id == place_id:
                reviews.append(review)
        return reviews
#-----------------------------------update_review-----------------------------------

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

#-----------------------------------update_review-----------------------------------
        
        updates = {}
        for field, value in review_data.items():
            if hasattr(review, field):
                updates[field] = value

        updated_review = self.review_repo.update(review_id, updates)

        if updated_review is None:
            updated_review = self.get_review(review_id)

        return updated_review
#-----------------------------------delete_review-----------------------------------

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

#-----------------------------------get_place_by_title-----------------------------------
    
    def get_place_by_title(self, title):
        return self.place_repo.get_by_attribute('title', title)

#-----------------------------------get_review_by_user_and_place-----------------------------------
    
    def get_review_by_user_and_place(self, user_id, place_id):
        """Get a review by user ID and place ID"""
        reviews = self.review_repo.get_all()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None