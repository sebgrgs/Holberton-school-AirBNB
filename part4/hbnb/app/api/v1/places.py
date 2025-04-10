from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

#----------------------------------------------amenity_model for input in Place------------------------------------------------

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

#----------------------------------------------user_model for input in Place------------------------------------------------

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

#----------------------------------------------review_model for input in Place------------------------------------------------

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

#----------------------------------------------place_model for input------------------------------------------------

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

#----------------------------------------------basic endpoint------------------------------------------------

@api.route('/')
class PlaceList(Resource):

#----------------------------------------------post method------------------------------------------------

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        try:
            place_title = facade.get_place_by_title(place_data['title'])
            if place_title:
                return {'error': 'Place with the same title already exists'}, 400
            user = facade.get_user(place_data['owner_id'])
            if place_data['owner_id'] != current_user['id']:
                return {'error': 'You can only create places for your own account'}, 403
            if not user:
                return {'error': 'Owner not found'}, 404
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

#----------------------------------------------get all places method------------------------------------------------

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id
        } for place in places], 200

#----------------------------------------------search for place_id endpoint------------------------------------------------

@api.route('/<place_id>')
class PlaceResource(Resource):

#----------------------------------------------get place by id method------------------------------------------------

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        owner = facade.get_user(place.owner_id) # bring the object by user id, not a string
        if not owner:
            return {'error': 'Owner not found'}, 404

        amenities = [{
            'id': str(amenity.id),
            'name': amenity.name
        } for amenity in place.amenities]

        return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                },
                'amenities': amenities
            }, 200

#----------------------------------------------delete method------------------------------------------------

    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'admin privileges required')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        current_user = get_jwt_identity()
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner_id != current_user['id'] and not current_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200

#----------------------------------------------put method------------------------------------------------

    @api.expect(place_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place_data = api.payload
        
        # First check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Check authorization
        if not current_user.get('is_admin') and place.owner_id != current_user.get('id'):
            return {'error': 'Unauthorized action'}, 403

        try:
            # Only check title if it's being updated
            if 'title' in place_data:
                place_title = facade.get_place_by_title(place_data['title'])
                if place_title and place_title.id != place_id:
                    return {'error': 'Place with the same title already exists'}, 400

            # Only check owner_id if it's being updated
            if 'owner_id' in place_data:
                user = facade.get_user(place_data['owner_id'])
                if not user:
                    return {'error': 'Owner not found'}, 404

            updated_place = facade.update_place(place_id, place_data)
            return {
                'id': str(updated_place.id),
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id,
                'amenities': [str(a) for a in updated_place.amenities]
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400

#----------------------------------------------get all reviews for a place endpoint------------------------------------------------

    @api.route('/<place_id>/reviews')
    class PlaceReviewList(Resource):

#----------------------------------------------get all reviews for a place method------------------------------------------------

        @api.response(200, 'List of reviews for the place retrieved successfully')
        @api.response(404, 'Place not found')
        def get(self, place_id):
            """Get all reviews for a specific place"""
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            reviews = facade.get_reviews_by_place(place_id)
            return [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in reviews], 200
