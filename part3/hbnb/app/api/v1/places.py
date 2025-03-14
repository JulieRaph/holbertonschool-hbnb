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
    @api.expect(models['create_place'])
    @api.response(201, 'Place successfully created', models['place_response'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Unauthorized action', models['unauthorized_action'])
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)
        
        if not user:
            api.abort(403, "Unauthorized action")

        place_data = api.payload
        place_data["owner_id"] = user.id
        amenities = []
        if 'amenities' in place_data:
            amenities = place_data.pop("amenities")

        try:    
            new_place = facade.create_place(place_data, amenities)
            place_dict = new_place.to_dict()
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return place_dict, 201

    @api.response(200, 'List of places retrieved successfully', models['places_list']['places'])
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        places_list = [place.dict() for place in all_places]
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', models['placeById_response'])
    @api.response(404, 'Place not found', models['not_found'])
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        
        if not place:
            api.abort(404, "Place not found")

        owner_data = place.owner.to_dict()
        reviews_data = [review.to_dict() for review in place.reviews]
        amenities_data = [amenity.to_dict() for amenity in place.place_amenities]
        place_dict = place.to_dict()
        place_dict['owner'] = owner_data
        place_dict['amenities'] = amenities_data
        place_dict['reviews'] = reviews_data

        return place_dict, 200

    @api.expect()
    @api.response(200, 'Place updated successfully', models['updated'])
    @api.response(404, 'Place not found', models['not_found'])
    @api.response(400, 'Invalid input data', models['invalid_input'])
    @api.response(403, 'Unauthorized action', models['unauthorized_action'])
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        place = facade.get_place(place_id)
        
        if not place:
            api.abort(404, "Place not found")

        if not user or place.owner_id != user.get('id'):
            api.abort(403,'Unauthorized action')

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

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully', models['place_reviews_list']['place_reviews'])
    @api.response(404, 'Place not found', models['not_found'])
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