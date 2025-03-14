from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from doc_models import initialize_models

api = Namespace('admin', description='Admin operations')
models = initialize_models(api)


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(models['admin_create_user'])
    @api.response(201, 'User successfully created', models['admin_create_user_response'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @jwt_required()
    def post(self):
        """Register a new user"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        
        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')
            
        user_data = api.payload
        email = user_data.get('email')
         
        if facade.get_user_by_email(email):
            api.abort(400, 'Email already registered')

        try:
            new_user = facade.create_user(user_data)
            user_dict = new_user.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return user_dict, 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(models['admin_update_user'])
    @api.response(201, 'User successfully updated', models['admin_update_user_response'])
    @api.response(404, 'User not found', models['not_found'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @jwt_required()
    def put(self, user_id):
        """Update an existin user"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        user = facade.get_user(user_id)
        
        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')
        
        if not user:
            api.abort(404, 'User not found')

        user_data = api.payload
        email = user_data.get('email')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user.id:
                api.abort(400, 'Email already in use')

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.to_dict()).to_dict()
            user_dict = updated_user.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return user_dict, 201

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(models['create_amenity'])
    @api.response(201, 'Amenity successfully created', models['amenity_response'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @jwt_required()
    def post(self):
        """Create amenity"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)

        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')

        amenity_data = api.payload

        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            api.abort(400, 'Amenity already registered')
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
            amenity_dict = new_amenity.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
            
        return amenity_dict, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect()
    @api.response(200, 'Amenity updated successfully', models['updated'])
    @api.response(404, 'Amenity not found', models['not_found'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        amenity = facade.get_amenity(amenity_id)

        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')

        if not amenity:
            api.abort(404, "Amenity not found")
        
        amenity_data = api.payload

        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity and existing_amenity.id != amenity.id:
            api.abort(400, "Amenity name already exists")

        try:
            facade.update_amenity(amenity_id, amenity_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
            
        return {"message": "Amenity updated successfully"}, 200

@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect()
    @api.response(200, 'Place updated successfully', models['updated'])
    @api.response(404, 'Place not found', models['not_found'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @jwt_required()
    def put(self, place_id):
        """Place update"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        place = facade.get_place(place_id)
        
        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')
        
        if not place:
            api.abort(404, "Place not found")

        place_data = api.payload
        amenities = []
        if 'amenities' in place_data:
            amenities = place_data.pop("amenities")

        if "owner_id" in place_data:
            api.abort(400, 'Invalid input data')

        try:
            place.update(place_data)
            facade.update_place(place_id, place.to_dict(), amenities)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Place updated successfully"}, 200

    @api.response(200, 'Place deleted successfully', models['deleted'])
    @api.response(404, 'Place not found', models['not_found'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @jwt_required()
    def delete(self, place_id):
        """Place delete"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        place = facade.get_place(place_id)

        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')
            
        if not place:
            api.abort(404, "Place not found")

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200

@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @api.expect()
    @api.response(200, 'Review updated successfully', models['updated'])
    @api.response(404, 'Review not found', models['not_found'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @jwt_required()
    def put(self, review_id):
        """Review update"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        review = facade.get_review(review_id)

        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')

        if not review:
            api.abort(404, "Review not found")

        review_data = api.payload

        valid_inputs = ["rating", "text"]
        for input in valid_inputs:
            if input not in review_data:
                api.abort(400, "Invalid input data")

        try:
            review.update(review_data)
            facade.update_review(review_id, review_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Review updated successfully"}, 200


    @api.response(200, 'Review deleted successfully', models['deleted'])
    @api.response(404, 'Review not found', models['not_found'])
    @api.response(403, 'Admin privileges required', models['admin_privileges'])
    @jwt_required()
    def delete(self, review_id):
        """Review delete"""
        current_user = get_jwt_identity().get('id')
        admin_user = facade.get_user(current_user)
        review = facade.get_review(review_id)

        if not admin_user or not admin_user.is_admin:
            api.abort(403, 'Admin privileges required')

        if not review:
            api.abort(404, "Review not found")

        facade.delete_review(review_id)
        
        return {"message": "Review deleted successfully"}, 200