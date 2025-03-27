from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from doc_models import initialize_models

api = Namespace('users', description='User operations')
models = initialize_models(api)


@api.route('/')
class UserList(Resource):
    @api.expect(models['UserCreate'])
    @api.response(201, 'User successfully created', models['UserResponse'])
    @api.response(400, 'Invalid input data', models['InvalidInput'])
    def post(self):
        """Register a new user"""
        user_data = api.payload
        email = user_data.get('email')

        valid_inputs = ['first_name', 'last_name', 'email', 'password']
        for input in user_data:
            if input not in valid_inputs:
                api.abort(400, f'Invalid input data: {input}')
        
        existing_user = facade.get_user_by_email(email)
        if existing_user:
            api.abort(400, 'Email already in use')
            
        try:
            new_user = facade.create_user(user_data)
            user_dict = new_user.to_dict()
            del user_dict['is_admin']
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return user_dict, 201
    
    @api.response(200, "Users retrieved successfully", models['UsersList'])
    def get(self):
        """Retrieve a list of all users"""
        all_users = facade.get_all_users()
        users_list = [user.to_dict() for user in all_users]
        for user in users_list:
            del user['is_admin'] 
        return users_list, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully', models['UserResponse'])
    @api.response(404, 'User not found', models['NotFound'])
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        user_dict = user.to_dict()
        del user_dict['is_admin']
        return user_dict, 200

    @api.expect(models['UserUpdate'])
    @api.response(201, 'User successfully updated', models['UserUpdateResponse'])
    @api.response(404, 'User not found', models['NotFound'])
    @api.response(400, 'Invalid input data', models['InvalidInput'])
    @api.response(403, 'Unauthorized action', models['UnauthorizedAction'])
    @jwt_required()
    @api.doc(security='token')
    def put(self, user_id):
        """Update a user"""
        current_user = get_jwt_identity().get('id')
        user = facade.get_user(current_user)

        if not facade.get_user(user_id):
            api.abort(404, 'User not found')

        """Get user details by ID"""
        if not user or user_id != user.id:
            api.abort(403, "Unauthorized action")

        user_data = api.payload
        
        valid_inputs = ["first_name", "last_name"]
        for input in user_data:
            if input not in valid_inputs:
                api.abort(400, f'Invalid input data: {input}')

        try:
            updated_user = facade.update_user(user_id, user_data)
            user_dict = updated_user.to_dict()
            del user_dict['is_admin']
        except (ValueError, TypeError) as e:
            api.abort(400, str(e))

        return user_dict, 201