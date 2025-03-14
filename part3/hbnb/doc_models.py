from flask_restx import fields, Api

def initialize_models(api: Api):
    create_user = api.model('Create User', {
        'first_name': fields.String(required=True, description="User first name", example="John"),
        'last_name': fields.String(required=True, description="User last name", example="Doe"),
        'email': fields.String(required=True, description="User email", example="john@email.com"),
        'password': fields.String(required=True, description="User password", example="Johnd0e!")
    })
    
    return {
        'create_user': create_user
    }