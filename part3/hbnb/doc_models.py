from flask_restx import fields, Api

def initialize_models(api: Api):
    login = api.model('Login', {
        'email': fields.String(required=True, description='User email', example="john@email.com"),
        'password': fields.String(required=True, description='User password', example="Johnd0e!")
    })
    
    create_user = api.model('CreateUser', {
        'first_name': fields.String(required=True, description="User first name", example="John"),
        'last_name': fields.String(required=True, description="User last name", example="Doe"),
        'email': fields.String(required=True, description="User email", example="john@email.com"),
        'password': fields.String(required=True, description="User password", example="Johnd0e!")
    })
    
    admin_create_user = api.model('AdminCreateUser', {
        'first_name': fields.String(required=True, description="User first name", example="Peter"),
        'last_name': fields.String(required=True, description="User last name", example="Parker"),
        'email': fields.String(required=True, description="User email", example="peter@email.com"),
        'password': fields.String(required=True, description="User password", example="Sp1derman!"),
        'is_admin': fields.Boolean(description="role authorization", example=True)
    })
    
    create_amenity = api.model('CreateAmenity', {
        'name': fields.String(required=True, description='Name of the amenity', example="Wifi")
    })
    
    create_place = api.model('CreatePlace', {
        'title': fields.String(required=True, description='Title of the place', example='Great house at the beach'),
        'description': fields.String(description='Description of the place', example='A nice place to stay'),
        'price': fields.Float(required=True, description='Price per night', example=100.0),
        'latitude': fields.Float(required=True, description='Latitude of the place', example=-90.0),
        'longitude': fields.Float(required=True, description='Longitude of the place', example=-122.4194),
        'amenities': fields.List(fields.String(description='List of amenity IDs'), example=["5191c141-a47b-465a-a94c-4007c6b69e1a"])
    })
    
    create_review = api.model('CreateReview', {
        'text': fields.String(required=True, description='Text of the review', example="Super cool!"),
        'rating': fields.Integer(required=True, description='Rating of the place (1-5)', example=5),
        'place_id': fields.String(required=True, description='ID of the place', example="a6e9d55e-c8d1-4268-bb65-4c19a5206a08")
    })
    
    
    login_response = api.model('LoginResponse200', {
        "access_token": fields.String(description='Token', example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTk2MTQ5MCwianRpIjoiZjZlM2Y4ZTEtZmM4MC00ODY3LTliZDktNGQwZDJkZGJhZDBhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6IjYwZjU2MDhiLTE5N2QtNGFjNC05MGQ0LWVjZjM4NWFiYWVlMyIsImlzX2FkbWluIjpmYWxzZX0sIm5iZiI6MTc0MTk2MTQ5MCwiY3NyZiI6IjRiZjllZmU0LTJkODAtNDBlMC1iMjE5LTgzNDc3MzliY2EyNSIsImV4cCI6MTc0MTk2MjM5MH0.N3xtpc6Ha-3wmXTSbz94Z_A7hkuswgrHrD6h4_XUlxk")
    })
    
    user_response = api.model('UserResponse201', {
        'id': fields.String(description="User id", example="7017d9b6-d116-4450-99f4-2e712c27a059"),
        'first_name': fields.String(description="User first name", example="John"),
        'last_name': fields.String(description="User last name", example="Doe"),
        'email': fields.String(description="User email", example="john@email.com")
    })
    
    admin_create_user_response = api.model('AdminCreateUserResponse201', {
        'id': fields.String(description="User id", example="7c3cf350-44af-4c1d-ace7-1c07ecb78160"),
        'first_name': fields.String(required=True, description="User first name", example="Peter"),
        'last_name': fields.String(required=True, description="User last name", example="Parker"),
        'email': fields.String(required=True, description="User email", example="peter@email.com"),
        'is_admin': fields.Boolean(description="role authorization", example=True)
    })
    
    admin_update_user_response = api.model('AdminUpdateUserResponse201', {
        'id': fields.String(description="User id", example="7c3cf350-44af-4c1d-ace7-1c07ecb78160"),
        'first_name': fields.String(description="User first name", example="Peter"),
        'last_name': fields.String(description="User last name", example="Parker"),
        'email': fields.String(description="User email", example="peter@spiderman.com"),
        'is_admin': fields.Boolean(description="role authorization", example=False)
    })
    
    amenity_response = api.model('ResponseAmenity201', {
        'id': fields.String(description="Amenity id", example="5191c141-a47b-465a-a94c-4007c6b69e1a"),
        'name': fields.String(description='Name of the amenity', example="Wifi") 
    })
    
    place_response = api.model('ResponsePlace201', {
        'id': fields.String(description="Place id", example="d6bf7e6e-13f4-4790-aae7-3a98f591df9c"),
        'title': fields.String(required=True, description='Title of the place', example='Great house at the beach'),
        'description': fields.String(description='Description of the place', example='A nice place to stay'),
        'price': fields.Float(required=True, description='Price per night', example=100.0),
        'latitude': fields.Float(required=True, description='Latitude of the place', example=-90.0),
        'longitude': fields.Float(required=True, description='Longitude of the place', example=-122.4194)
    })
    
    review_response = api.model('ReviewResonse201', {
        'id': fields.String(description="Review id", example="7293b0c5-f782-1823-87j9-3a934x85c756"),
        'rating': fields.String(description="Rating", example="5"),
        'text': fields.String(description="Text", example="Super cool!"),
        'place_id': fields.String(description="Place id", example="a6e9d55e-c8d1-4268-bb65-4c19a5206a08"),
        'user_id': fields.String(description="User id", example="7017d9b6-d116-4450-99f4-2e712c27a059")
    })
    
    review_response_2 = api.model('ReviewResonse201', {
        'id': fields.String(description="Review id", example="7293b0c5-f782-1823-87j9-3a934x85c756"),
        'rating': fields.String(description="Rating", example="5"),
        'text': fields.String(description="Text", example="Super cool!"),
    })
    
    invalid_credentials = api.model('InvalidaCredentials401', {
        'message': fields.String(description="Error msg", example="Invalid credentials")
    })
    
    invalid_input = api.model('InvalidInput400', {
        'message': fields.String(description="Error msg", example="<error_message>")
    })
    
    not_found = api.model('NotFound404', {
        'message': fields.String(description="Error msg", example="<entity> not found")
    })
    
    unauthorized_action = api.model('UnauthorizedAction403', {
        'message': fields.String(description="Error msg", example="Unauthorized action")
    })
    
    admin_privileges = api.model('AdminPrivileges403', {
        'message': fields.String(description="Error msg", example="Admin privileges required")
    })
    
    updated = api.model('UpdateSuccess200', {
        'message': fields.String(description="Update success", example="<entity> updated successfully")
    })
    
    deleted = api.model('DeleteSuccess200', {
        'message': fields.String(description="Delete success", example="<entity> deleted successfully")
    })
    
    users_list = api.model('UsersList', {
        'users': fields.List(fields.Nested(user_response))
    })
    
    amenities_list = api.model('AmenitiesList', {
        'amenities': fields.List(fields.Nested(amenity_response))
    })
    
    places_list = api.model('PlacesList', {
        'places': fields.List(fields.Nested(place_response))
    })
    
    reviews_list = api.model('ReviewsList', {
        'reviews': fields.List(fields.Nested(review_response))
    })
    
    place_reviews_list = api.model('PlaceReviewList', {
        'place_reviews': fields.List(fields.Nested(review_response_2))
    })
    
    update_user = api.model('UpdateUser', {
        'first_name': fields.String(description='First name of the user', example="Jane"),
        'last_name': fields.String(description='Last name of the user', example="Doe"),
    })
    
    admin_update_user = api.model('UpdateUser', {
        'first_name': fields.String(required=True, description="User first name", example="Peter"),
        'last_name': fields.String(required=True, description="User last name", example="Parker"),
        'email': fields.String(required=True, description="User email", example="peter@spiderman.com"),
        'password': fields.String(required=True, description="User password", example="Sp1derman!"),
        'is_admin': fields.Boolean(description="role authorization", example=False)
    })
    
    update_amenity = api.model('UpdateAmenity', {
        'name': fields.String(required=True, description='Name of the amenity', example="Wi-Fi")
    })
    
    placeById_response = api.model('ResponsePlaceByID200', {
        'id': fields.String(description="Place id", example="a6e9d55e-c8d1-4268-bb65-4c19a5206a08"),
        'title': fields.String(required=True, description='Title of the place', example='Great house at the beach'),
        'description': fields.String(description='Description of the place', example='A nice place to stay'),
        'price': fields.Float(required=True, description='Price per night', example=100.0),
        'latitude': fields.Float(required=True, description='Latitude of the place', example=-90.0),
        'longitude': fields.Float(required=True, description='Longitude of the place', example=-122.4194),
        'owner': fields.Nested(user_response),
        'amenities': fields.List(fields.Nested(amenity_response), description='List of detailed amenities'),
        'reviews': fields.List(fields.Nested(review_response), description='List of detailed reviews'),
    })
    
    return {
        'login': login,
        'create_user': create_user,
        'admin_create_user': admin_create_user,
        'create_amenity': create_amenity,
        'create_place': create_place,
        'create_review': create_review,
        'login_response': login_response,
        'user_response': user_response,
        'admin_create_user_response': admin_create_user_response,
        'admin_update_user_response': admin_update_user_response,
        'place_response': place_response,
        'review_response': review_response,
        'amenity_response': amenity_response,
        'users_list': users_list,
        'amenities_list': amenities_list,
        'places_list': places_list,
        'reviews_list': reviews_list,
        'place_reviews_list': place_reviews_list,
        'invalid_credentials': invalid_credentials,
        'invalid_input': invalid_input,
        'update_user': update_user,
        'admin_update_user': admin_update_user,
        'update_amenity': update_amenity,
        'updated': updated,
        'deleted': deleted,
        'not_found': not_found,
        'unauthorized_action': unauthorized_action,
        'admin_privileges': admin_privileges,
        'placeById_response': placeById_response,
        
    }