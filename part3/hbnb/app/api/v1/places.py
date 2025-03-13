from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
import uuid

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

place_update_model = api.model('Place Update', {
    'title': fields.String(description='Title of the place', example="Super Apartment"),
    'description': fields.String(description='Description of the place', example="A super place for your week-end!"),
    'price': fields.Float(description='Price per night', example=150.0),
    'latitude': fields.Float(description='Latitude of the place', example=37.7749),
    'longitude': fields.Float(description='Longitude of the place', example=-122.4194),
    'amenities': fields.List(fields.String, description="List of amenities ID's", example=["1fa85f64-5717-4562-b3fc-2c963f66afa6"]),
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)
        
        if not user:
            api.abort(403, "Unauthorized action")

        place_data = api.payload
        place_data["owner_id"] = user.id
        amenities = place_data.pop("amenities")

        try:    
            new_place = facade.create_place(place_data, amenities)
            new_place_data = new_place.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_place_data, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        return [{'id': place.id,
                 'title': place.title,
                 'latitude': place.latitude,
                 'longitude': place.longitude} for place in all_places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        
        if not place:
            api.abort(404, "Place not found")

        user_data = place.owner.to_dict()
        reviews_data = [review.to_dict() for review in place.reviews]
        amenities_data = [amenity.to_dict() for amenity in place.place_amenities]            

        return {'id': place.id,
                'title': place.title,
                'descripton': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': user_data,
                'amenities': amenities_data,
                'reviews': reviews_data
                }, 200

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        # if place.owner_id != current_user.get('id'):
        if not current_user:
            api.abort(403,'Unauthorized action')

        place_data = api.payload
        
        if "owner_id" in place_data:
            api.abort(400, 'Invalid input data')

        amenities = place_data.get("amenities")
        if amenities:
            for amenity_id in amenities:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity_id)

        try:
            place.update(place_data)
            facade.update_place(place_id, place.to_dict())
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Place updated successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            api.abort(404, 'Place not found')
        
        reviews = facade.get_reviews_by_place(place.id)
        place_reviews = [
            {key: value for key, value in review.to_dict().items() if key not in ["user_id", "place_id"]}
            for review in reviews
        ]

        return place_reviews, 200