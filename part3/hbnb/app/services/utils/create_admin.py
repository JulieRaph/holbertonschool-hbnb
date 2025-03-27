import os
from app.models.user import User
from app import db
from flask import current_app

def create_admin_user():
    with current_app.app_context():
        admin_exists = User.query.filter_by(email=os.getenv('ADMIN_EMAIL')).first()
        if not admin_exists:
            admin = User(first_name='Admin', last_name='HBnB', email=os.getenv('ADMIN_EMAIL'), is_admin=True)
            admin.hash_password(os.getenv('ADMIN_PASSWORD'))
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin user already exists") 