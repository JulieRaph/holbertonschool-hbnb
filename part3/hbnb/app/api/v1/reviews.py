from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from doc_models import initialize_models
from app import db

api = Namespace('reviews', description='User operations')
models = initialize_models(api)


@api.route('/')
class ReviewList(Resource):
    @api.expect(models['ReviewCreate'])
    @api.response(201, 'Review successfully created', models['ReviewResponse'])
    @api.response(400, 'Invalid input data', models['InvalidInput'])
    @api.response(403, 'Unauthorized action', models['UnauthorizedAction'])
    @jwt_required()
    @api.doc(security='token')
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

    @api.response(200, 'List of reviews retrieved successfully', models['ReviewsList'])
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        reviews_list = [review.to_dict() for review in all_reviews]
        return reviews_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', models['ReviewResponse'])
    @api.response(404, 'Review not found', models['NotFound'])
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        
        if not review:
            api.abort(404, 'Review not found')
        
        review_dict = review.to_dict()

        return review_dict, 200

    @api.expect(models['ReviewUpdate'])
    @api.response(200, 'Review updated successfully', models['Updated'])
    @api.response(404, 'Review not found', models['NotFound'])
    @api.response(400, 'Invalid input data', models['InvalidInput'])
    @api.response(403, 'Unauthorized action', models['UnauthorizedAction'])
    @jwt_required()
    @api.doc(security='token')
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

    @api.response(200, 'Review deleted successfully', models['Deleted'])
    @api.response(404, 'Review not found', models['NotFound'])
    @api.response(403, 'Unauthorized action', models['UnauthorizedAction'])
    @jwt_required()
    @api.doc(security='token')
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