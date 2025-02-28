from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        
        user = facade.get_user(place_data.get("owner_id"))
        if not user:
            api.abort(400, "Invalid user")
        
        invalid_amenities = []
        if "amenities" in place_data:
            for amenity_id in place_data.get("amenities"):
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    invalid_amenities.append(amenity_id)
            if invalid_amenities:
                api.abort(400, f"Invalid amenities: {invalid_amenities}")

        try:    
            new_place = facade.create_place(place_data)
            user.add_place(new_place.id)
            user_data = user.to_dict()
            facade.update_user(user.id, user_data)
            new_place_data = new_place.to_dict()
            del new_place_data["amenities"]
            del new_place_data["reviews"]
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

        user = facade.get_user(place.owner_id)
        user_data = user.to_dict()
        amenities_data = []
        for amenity_id in place.amenities:
            amenity = facade.get_amenity(amenity_id)
            if amenity:
                amenities_data.append(amenity.to_dict())
        
        reviews_data = []
        for review_id in place.reviews:
            review = facade.get_review(review_id)
            if review:
                review_data = review.to_dict()
                del review_data['place_id']
                reviews_data.append(review_data)
            

        return {'id': place.id, 'title': place.title,
                'descripton': place.description, 'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude, 'owner': user_data,
                'amenities': amenities_data,
                'reviews': reviews_data}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
            
        if "owner_id" in place_data:
            api.abort(400, "Owner can not be modified")
        
        if "amenities" in place_data:
            invalid_amenities = []
            for amenity_id in place_data.get("amenities"):
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    invalid_amenities.append(amenity_id)
            if invalid_amenities:
                api.abort(400, f"Invalid amenities: {invalid_amenities}")

        try:
            place.update(place_data)
            facade.update_place(place_id, place.to_dict())
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))
        
        return {"message": "Place updated successfully"}, 200
