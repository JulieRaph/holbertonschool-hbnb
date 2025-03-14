from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from doc_models import initialize_models

api = Namespace('auth', description='Authentication operations')
models = initialize_models(api)

@api.route('/login')
class Login(Resource):
    @api.expect(models['login'])
    @api.response(200, 'User successfully loged', models['login_response'])
    @api.response(401, 'Invalid credentials', models['invalid_credentials'])
    def post(self):
        """Authenticate user and return a JWT token"""
        print("Login request received")
        credentials = api.payload
        
        user = facade.get_user_by_email(credentials['email'])
        
        if not user or not user.verify_password(credentials['password']):
            api.abort(401, "Invalid credentials")

        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        
        return {'access_token': access_token}, 200