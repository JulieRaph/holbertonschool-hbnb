from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', example="John"),
    'last_name': fields.String(required=True, description='Last name of the user', example="Doe"),
    'email': fields.String(required=True, description='Email of the user', example="john@email.com")
})

user_update_model = api.model('User Update', {
    'first_name': fields.String(description='First name of the user', example="Jane"),
    'last_name': fields.String(description='Last name of the user', example="Doe"),
    'email': fields.String(description='Email of the user', example="jane@email.com")
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return new_user.to_dict(), 201
    
    @api.response(200, "Users retrieved successfully")
    def get(self):
        """Retrieve a list of all users"""
        all_users = facade.get_all_users()
        return [{
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        } for user in all_users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to_dict(), 200

    @api.expect(user_update_model)
    @api.response(201, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user"""
        user_data = api.payload
        
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        if "email" in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user.id:
                api.abort(400, "Email already registered by another user")

        try:
            user.update(user_data)
            updated_user = facade.update_user(user_id, user.to_dict())
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return updated_user.to_dict(), 201
