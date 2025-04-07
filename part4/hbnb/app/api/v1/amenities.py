from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

#----------------------------------------------amenity_model for input------------------------------------------------

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

#----------------------------------------------basic endpoint------------------------------------------------

@api.route('/')
class AmenityList(Resource):

#----------------------------------------------post method------------------------------------------------

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

#----------------------------------------------get method------------------------------------------------

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200

#----------------------------------------------search for amenity_id endpoint------------------------------------------------

@api.route('/<amenity_id>')
class AmenityResource(Resource):

#----------------------------------------------get method------------------------------------------------

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

#----------------------------------------------delete method------------------------------------------------
    
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity"""
        current_user = get_jwt_identity()
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200

#----------------------------------------------put method------------------------------------------------

    @api.expect(amenity_model, validate=False)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
    