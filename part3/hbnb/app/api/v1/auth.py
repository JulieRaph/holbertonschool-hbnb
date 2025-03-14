from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email', example="john@email.com"),
    'password': fields.String(required=True, description='User password', example="Johnd0e!")
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'User successfully loged')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        print("Login request received")
        credentials = api.payload
        
        user = facade.get_user_by_email(credentials['email'])
        
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        
        return {'access_token': access_token}, 200