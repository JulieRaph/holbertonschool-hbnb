from flask_restx import fields, Api

def initialize_models(api: Api):
    Login = api.model('Login', {
        'email': fields.String(required=True, description='User email', example="john@email.com"),
        'password': fields.String(required=True, description='User password', example="Johnd0e!")
    })
    
    UserId = api.model('UserId', {
        'id': fields.String(description="User id", example="07e1277b-77e7-47fa-9493-8d685ee2bba5"),
    })
    
    AdminId = api.model('AdminId', {
        'id': fields.String(description="Admin id", example="36c9050e-ddd3-4c3b-9731-9f487208bbc1"),
    })
    
    AmenityId = api.model('AmenityId', {
        'id': fields.String(description="Amenity id", example="99493758-3936-4aac-8a07-835b84ce02ef"),
    })
    
    PlaceId = api.model('PlaceId', {
        'id': fields.String(description="Place id", example="32491cac-9dfa-4c76-bcd6-499421c5c269"),
    })
    
    ReviewId = api.model('ReviewId', {
        'id': fields.String(description="Review id", example="82fe063d-fe6e-4b84-a12d-4400df168834"),
    })
    
    UserCreate = api.model('UserCreate', {
        'first_name': fields.String(required=True, description="User first name", example="John"),
        'last_name': fields.String(required=True, description="User last name", example="Doe"),
        'email': fields.String(required=True, description="User email", example="john@email.com"),
        'password': fields.String(required=True, description="User password", example="Johnd0e!")
    })
    
    AdminUserCreate = api.model('AdminUserCreate', {
        'first_name': fields.String(required=True, description="User first name", example="Peter"),
        'last_name': fields.String(required=True, description="User last name", example="Parker"),
        'email': fields.String(required=True, description="User email", example="peter@email.com"),
        'password': fields.String(required=True, description="User password", example="Sp1derman!"),
        'is_admin': fields.Boolean(description="role authorization", example=True)
    })
    
    AmenityCreate = api.model('AmenityCreate', {
        'name': fields.String(required=True, description='Name of the amenity', example="Wifi")
    })
    
    PlaceCreate = api.model('PlaceCreate', {
        'title': fields.String(required=True, description='Title of the place', example='Great house'),
        'description': fields.String(description='Description of the place', example='A nice place to stay'),
        'price': fields.Float(required=True, description='Price per night', example=100.0),
        'latitude': fields.Float(required=True, description='Latitude of the place', example=-75.102),
        'longitude': fields.Float(required=True, description='Longitude of the place', example=-122.4194)
    })
    
    PlaceUpdate = api.model('PlaceUpdate', {
        'title': fields.String(description='Title of the place', example='Great house at the beach'),
        'description': fields.String(description='Description of the place', example='A nice place for holidays'),
        'price': fields.Float(description='Price per night', example=150.0),
        'latitude': fields.Float(description='Latitude of the place', example=-75.102),
        'longitude': fields.Float(description='Longitude of the place', example=-122.4194),
        'amenities': fields.List(fields.String(description='List of amenity IDs'), example=["99493758-3936-4aac-8a07-835b84ce02ef"])
    })
    
    ReviewCreate = api.model('ReviewCreate', {
        'text': fields.String(required=True, description='Text of the review', example="Super cool!"),
        'rating': fields.Integer(required=True, description='Rating of the place (1-5)', example=5),
        'place_id': fields.String(required=True, description='ID of the place', example="32491cac-9dfa-4c76-bcd6-499421c5c269")
    })
    
    ReviewUpdate = api.model('ReviewUpdate', {
        'text': fields.String(description='Text of the review', example="Not So Good"),
        'rating': fields.Integer(description='Rating of the place (1-5)', example=3),
    })
    
    LoginResponse = api.model('LoginResponse', {
        "access_token": fields.String(description='Token', example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTk2MTQ5MCwianRpIjoiZjZlM2Y4ZTEtZmM4MC00ODY3LTliZDktNGQwZDJkZGJhZDBhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6IjYwZjU2MDhiLTE5N2QtNGFjNC05MGQ0LWVjZjM4NWFiYWVlMyIsImlzX2FkbWluIjpmYWxzZX0sIm5iZiI6MTc0MTk2MTQ5MCwiY3NyZiI6IjRiZjllZmU0LTJkODAtNDBlMC1iMjE5LTgzNDc3MzliY2EyNSIsImV4cCI6MTc0MTk2MjM5MH0.N3xtpc6Ha-3wmXTSbz94Z_A7hkuswgrHrD6h4_XUlxk")
    })
    
    UserResponse = api.inherit('UserResponse', UserId, {
        'first_name': fields.String(description="User first name", example="John"),
        'last_name': fields.String(description="User last name", example="Doe"),
        'email': fields.String(description="User email", example="john@email.com")
    })
    
    AdminUserCreateResponse = api.inherit('AdminUserCreateResponse', AdminId, {
        'first_name': fields.String(required=True, description="User first name", example="Peter"),
        'last_name': fields.String(required=True, description="User last name", example="Parker"),
        'email': fields.String(required=True, description="User email", example="peter@email.com"),
        'is_admin': fields.Boolean(description="role authorization", example=True)
    })
    
    AdminUserUpdateResponse = api.inherit('AdminUserUpdateResponse', AdminId, {
        'first_name': fields.String(description="User first name", example="Peter"),
        'last_name': fields.String(description="User last name", example="Parker"),
        'email': fields.String(description="User email", example="peter@spiderman.com"),
        'is_admin': fields.Boolean(description="role authorization", example=False)
    })
    
    AmenityResponse = api.inherit('AmenityResponse', AmenityId, {
        'name': fields.String(description='Name of the amenity', example="Wifi") 
    })
    
    PlaceResponse = api.inherit('PlaceResponse', PlaceId, {
        'title': fields.String(description='Title of the place', example='Great house at the beach'),
        'description': fields.String(description='Description of the place', example='A nice place to stay'),
        'price': fields.Float(description='Price per night', example=100.0),
        'latitude': fields.Float(description='Latitude of the place', example=-75.102),
        'longitude': fields.Float(description='Longitude of the place', example=-122.4194)
    })
    
    ReviewResponse = api.inherit('ReviewResponse', ReviewId, {
        'rating': fields.Integer(description="Rating", example=5),
        'text': fields.String(description="Text", example="Super cool!"),
        'place_id': fields.String(description="Place id", example="a6e9d55e-c8d1-4268-bb65-4c19a5206a08"),
        'user_id': fields.String(description="User id", example="c28c8c27-b900-409b-ab4d-cc215cb2f518")
    })
    
    InvalidCredentials = api.model('InvalidCredentials', {
        'message': fields.String(description="Error msg", example="Invalid credentials")
    })
    
    InvalidInput = api.model('InvalidInput', {
        'message': fields.String(description="Error msg", example="<error_message>")
    })
    
    NotFound = api.model('NotFound', {
        'message': fields.String(description="Error msg", example="<entity> not found")
    })
    
    UnauthorizedAction = api.model('UnauthorizedAction', {
        'message': fields.String(description="Error msg", example="Unauthorized action")
    })
    
    AdminPrivileges = api.model('AdminPrivileges', {
        'message': fields.String(description="Error msg", example="Admin privileges required")
    })
    
    Updated = api.model('Updated', {
        'message': fields.String(description="Update success", example="<entity> updated successfully")
    })
    
    Deleted = api.model('Deleted', {
        'message': fields.String(description="Delete success", example="<entity> deleted successfully")
    })
    
    UsersList = api.model('UsersList', {
        'Users': fields.List(fields.Nested(UserResponse))
    })
    
    AmenitiesList = api.model('AmenitiesList', {
        'Amenities': fields.List(fields.Nested(AmenityResponse))
    })
    
    PlacesList = api.model('PlacesList', {
        'Places': fields.List(fields.Nested(PlaceResponse))
    })
    
    ReviewsList = api.model('ReviewsList', {
        'Reviews': fields.List(fields.Nested(ReviewResponse))
    })
    
    UserUpdate = api.model('UserUpdate', {
        'first_name': fields.String(description='First name of the user', example="Jane"),
        'last_name': fields.String(description='Last name of the user', example="Doe"),
    })
    
    UserUpdateResponse = api.inherit('UserUpdateResponse', UserId, {
        'first_name': fields.String(description='First name of the user', example="Jane"),
        'last_name': fields.String(description='Last name of the user', example="Doe"),
        'email': fields.String(description="User email", example="john@email.com")
    })
    
    AdminUserUpdate = api.model('AdminUserUpdate', {
        'first_name': fields.String(description="User first name", example="Peter"),
        'last_name': fields.String(description="User last name", example="Parker"),
        'email': fields.String(description="User email", example="peter@spiderman.com"),
        'password': fields.String(description="User password", example="Sp1derman!"),
        'is_admin': fields.Boolean(description="role authorization", example=False)
    })
    
    AmenityUpdate = api.model('AmenityUpdate', {
        'name': fields.String(description='Name of the amenity', example="Wi-Fi")
    })
    
    PlaceByIdResponse = api.model('PlaceByIdResponse', {
        'id': fields.String(description="Place id", example="a6e9d55e-c8d1-4268-bb65-4c19a5206a08"),
        'title': fields.String(description='Title of the place', example='Great house at the beach'),
        'description': fields.String(description='Description of the place', example='A nice place to stay'),
        'price': fields.Float(description='Price per night', example=100.0),
        'latitude': fields.Float(description='Latitude of the place', example=-75.102),
        'longitude': fields.Float(description='Longitude of the place', example=-122.4194),
        'owner': fields.Nested(UserResponse),
        'amenities': fields.List(fields.Nested(AmenityResponse), description='List of detailed amenities'),
        'reviews': fields.List(fields.Nested(ReviewResponse), description='List of detailed reviews'),
    })
    
    ReviewsPlaceList = api.model('ReviewsPlaceList', {
        'ReviewsPlace': fields.List(fields.Raw, example=[
            {
                'id': "82fe063d-fe6e-4b84-a12d-4400df168834",
                'rating': 5,
                'text': "Super cool!",
                'user_id': "c28c8c27-b900-409b-ab4d-cc215cb2f518"
            }
        ])
    })
    
    return {
        # CommonRes
        "InvalidInput": InvalidInput,
        "NotFound": NotFound,
        "UnauthorizedAction": UnauthorizedAction,
        "InvalidCredentials": InvalidCredentials,
        "AdminPrivileges": AdminPrivileges,
        "Updated": Updated,
        "Deleted": Deleted,
        # User
        "UserCreate": UserCreate,
        "UserResponse": UserResponse,
        "UsersList": UsersList['Users'],
        "UserUpdate": UserUpdate,
        "UserUpdateResponse": UserUpdateResponse,
        # Login
        "Login": Login,
        "LoginResponse": LoginResponse,
        # Amenity
        "AmenitiesList": AmenitiesList['Amenities'],
        "AmenityResponse": AmenityResponse,
        # Place
        "PlaceCreate": PlaceCreate,
        "PlaceUpdate": PlaceUpdate,
        "PlaceResponse": PlaceResponse,
        "PlacesList": PlacesList['Places'],
        "PlaceByIdResponse": PlaceByIdResponse,
        "ReviewsPlaceList": ReviewsPlaceList['ReviewsPlace'],
        # Review
        "ReviewCreate": ReviewCreate,
        "ReviewResponse": ReviewResponse,
        "ReviewsList": ReviewsList['Reviews'],
        "ReviewUpdate": ReviewUpdate,
        # Admin
        "AdminUserCreate": AdminUserCreate,
        "AdminUserCreateResponse": AdminUserCreateResponse,
        "AdminUserUpdate": AdminUserUpdate,
        "AdminUserUpdateResponse": AdminUserUpdateResponse,
        "AmenityCreate": AmenityCreate,
        "AmenityResponse": AmenityResponse,
        "AmenityUpdate": AmenityUpdate,
        
    }