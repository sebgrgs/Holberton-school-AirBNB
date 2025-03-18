from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

#----------------------------------------------review_model for input------------------------------------------------

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

#----------------------------------------------basic endpoint------------------------------------------------

@api.route('/')
class ReviewList(Resource):

#----------------------------------------------post method------------------------------------------------

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        new_user = facade.get_user(review_data['user_id'])
        current_user = get_jwt_identity()
        if place.owner_id == current_user['id']:
            return {'error': 'You cannot create reviews for your own places'}, 400
        existing_review = facade.get_review_by_user_and_place(
            user_id=review_data['user_id'], place_id=review_data['place_id']
        )
        if existing_review:
            return {'error': 'User has already reviewed this place'}, 400
        if not new_user:
            return {'error': 'User not found'}, 404
        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

#----------------------------------------------get all reviews method------------------------------------------------

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        } for review in reviews], 200

#----------------------------------------------search for review_id endpoint------------------------------------------------

@api.route('/<review_id>')
class ReviewResource(Resource):

#----------------------------------------------get method for review by id method------------------------------------------------

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200
        else:
            return {'error': 'Review not found'}, 404

#----------------------------------------------put method by id------------------------------------------------

    @api.expect(review_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review_data = api.payload

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review_data['user_id'] != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        try:
            user = facade.get_user(review_data['user_id'])
            if not user:
                return {'error': 'User not found'}, 404
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404
            updated_review = facade.update_review(review_id, review_data)  
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

#----------------------------------------------delete by id method------------------------------------------------

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        current_user = get_jwt_identity()
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user_id != current_user['id'] and not current_user.get('is_admin'):
            return {'error': 'Unauthorized action'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

#---------------------------------------------- endpoint to get all reviews from a place id------------------------------------------------

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):

#----------------------------------------------get all reviews for a place method------------------------------------------------

#WARNING: DO NOT DELETE THIS METHOD, this is NOT AN ERROR

# This method is implemented in both place and review, it's an add that I found useful to have in both reviews and places
# It's a common operation to get all reviews for a place.

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        review_exists = facade.get_place(place_id)
        if reviews:
            return [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in reviews], 200
        elif not review_exists:
            return {'error': 'Place not found'}, 404
        else:
            return {'error': 'No reviews found for this place'}, 404
        
    