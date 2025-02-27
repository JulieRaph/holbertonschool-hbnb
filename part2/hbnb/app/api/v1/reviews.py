from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

update_review_model = api.model('Review_update', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        place = facade.get_place(review_data.get("place_id"))
        if not place:
            api.abort(400, "Invalid place")
            
        user = facade.get_user(review_data.get("user_id"))
        if not user or user.id == place.owner_id:
            api.abort(400, "Invalid user")

        try:
            new_review = facade.create_review(review_data)
            place.add_review(new_review.id)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return {'id': new_review.id, 'place_id': new_review.place_id,
                'rating': new_review.rating, 'text': new_review.text,
                'user_id': new_review.user_id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        return [{'id': review.id, 'place_id': review.place_id,
                 'rating': review.rating, 'text': review.text, 
                 'user_id': review.user_id} for review in all_reviews]

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'place_id': review.place_id,
                 'rating': review.rating, 'text': review.text, 
                 'user_id': review.user_id}, 200

    @api.expect(update_review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        review_data = {'user_id': review.user_id, 'place_id': review.place_id, 'text': data["text"], 'rating': data["rating"]}
        
        try:
            facade.update_review(review_id, review_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        
        review = facade.get_review(review_id)
        place = facade.get_place(review.place_id)

        if not review:
            api.abort(404,"Review not found")
        facade.delete_review(review_id)
        place.remove_review(review_id)
        return {"message": "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        
        review = facade.get_reviews_by_place(place_id)

        return [{'id': review.id, 'text': review.text,
                 'rating': review.rating} for review in review], 200
