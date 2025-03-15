from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
import uuid
from doc_models import initialize_models

api = Namespace('places', description='Place operations')
models = initialize_models(api)


@api.route('/')
class PlaceList(Resource):
    @api.expect(models['PlaceCreate'])
    @api.response(201, 'Place successfully created', models['PlaceResponse'])
    @api.response(400, 'Invalid input data', models['InvalidInput'])
    @api.response(403, 'Unauthorized action', models['UnauthorizedAction'])
    @jwt_required()
    @api.doc(security='token')
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)
        
        if not user:
            api.abort(403, "Unauthorized action")

        place_data = api.payload
        place_data["owner_id"] = user.id
        amenities = place_data.pop("amenities", [])

        try:    
            new_place = facade.create_place(place_data, amenities)
            place_dict = new_place.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return place_dict, 201

    @api.response(200, 'List of places retrieved successfully', models['PlacesList'])
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        places_list = [place.to_dict() for place in all_places]
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', models['PlaceByIdResponse'])
    @api.response(404, 'Place not found', models['NotFound'])
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        
        if not place:
            api.abort(404, "Place not found")

        owner_data = place.owner.to_dict()
        del owner_data['is_admin']
        reviews_data = [review.to_dict() for review in place.reviews]
        for review in reviews_data:
            del review['place_id'] 
        amenities_data = [amenity.to_dict() for amenity in place.place_amenities]
        place_dict = place.to_dict()
        place_dict['owner'] = owner_data
        place_dict['amenities'] = amenities_data
        place_dict['reviews'] = reviews_data

        return place_dict, 200

    @api.expect(models['PlaceUpdate'])
    @api.response(200, 'Place updated successfully', models['Updated'])
    @api.response(404, 'Place not found', models['NotFound'])
    @api.response(400, 'Invalid input data', models['InvalidInput'])
    @api.response(403, 'Unauthorized action', models['UnauthorizedAction'])
    @jwt_required()
    @api.doc(security='token')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)
        place = facade.get_place(place_id)
        
        if not place:
            api.abort(404, "Place not found")

        if not user or place.owner_id != user.id:
            api.abort(403,'Unauthorized action')

        place_data = api.payload
        amenities = place_data.pop("amenities", [])
        
        if "owner_id" in place_data:
            api.abort(400, 'Invalid input data')

        try:
            facade.update_place(place_id, place_data, amenities)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Place updated successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully', models['ReviewsPlaceList'])
    @api.response(404, 'Place not found', models['NotFound'])
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            api.abort(404, 'Place not found')
        
        reviews = facade.get_reviews_by_place(place.id)
        place_reviews_list = [
            {key: value for key, value in review.to_dict().items() if key not in ["user_id", "place_id"]}
            for review in reviews
        ]

        return place_reviews_list, 200