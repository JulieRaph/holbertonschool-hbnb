from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from doc_models import initialize_models
from app import db

api = Namespace('reviews', description='User operations')
models = initialize_models(api)

review_update_model = api.model('Review Update', {
    'text': fields.String(description='Text of the review', example="Not so cool!"),
    'rating': fields.Integer(description='Rating of the place (1-5)', example=3),
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place', example="Cozy Apartment"),
    'description': fields.String(description='Description of the place', example="A nice place to stay"),
    'price': fields.Float(required=True, description='Price per night', example=100.0),
    'latitude': fields.Float(required=True, description='Latitude of the place', example=37.7749),
    'longitude': fields.Float(required=True, description='Longitude of the place', example=-122.4194),
    'owner_id': fields.String(required=True, description='Owner of the place', example="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
    'amenities': fields.List(fields.String, description="List of amenities ID's", example=["1fa85f64-5717-4562-b3fc-2c963f66afa6"]),
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(models['create_review'])
    @api.response(201, 'Review successfully created', models['review_response'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Unauthorized action', models['unauthorized_action'])
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)
        
        review_data = api.payload
        
        place = facade.get_place(review_data.get("place_id"))
        
        if not place:
            api.abort(400, "Invalid place")
        
        if not user or user.id == place.owner_id:
            api.abort(403, "Unauthorized action")
        
        review_data["user_id"] = user.id

        place_reviews = facade.get_reviews_by_place(place.id)
        if any(review.user_id == user.id for review in place_reviews):
            api.abort(400, "Place already reviewed")
        
        review_data["place_id"] = place.id

        try:
            new_review = facade.create_review(review_data)
            review_dict = new_review.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return review_dict, 201

    @api.response(200, 'List of reviews retrieved successfully', models['reviews_list']['reviews'])
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        reviews_list = [review.to_dict() for review in all_reviews]
        return reviews_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', models['review_response'])
    @api.response(404, 'Review not found', models['not_found'])
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404, 'Review not found')
        
        review_dict = review.to_dict()

        return review_dict, 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully', models['updated'])
    @api.response(404, 'Review not found', models['not_found'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Unauthorized action', models['unauthorized_action'])
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)        
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404, "Review not found")

        if not user or user.id != review.user_id:
            api.abort(403,'Unauthorized action')

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
    @api.response(403, 'Unauthorized action', models['unauthorized_action'])
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404,"Review not found")

        if not user or user.id != review.user_id:
            api.abort(403,'Unauthorized action')

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200