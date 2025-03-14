#!/usr/bin/python3
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import facade
from doc_models import initialize_models

api = Namespace('amenities', description='Amenity operations')
models = initialize_models(api)

@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully', models['amenities_list']['amenities'])
    def get(self):
        """Retrieve a list of all amenities"""
        all_amenities = facade.get_all_amenities()
        amenities_list = [amenity.to_dict() for amenity in all_amenities]
        return amenities_list, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', models['amenity_response'])
    @api.response(404, 'Amenity not found', models['not_found'])
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        amenity_dict = amenity.to_dict()
        return amenity_dict, 200