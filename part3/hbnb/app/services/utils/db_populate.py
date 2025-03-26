from app.models.user import User
from app.models.amenity import Amenity
from app import db
from flask import current_app

amenities = [
    {"name": "WiFi"}, {"name": "Swimming Pool"}, {"name": "Air Conditioning"}
]

def db_populate():
    with current_app.app_context():
        admin_exists = User.query.filter_by(email="admin@hbnb.io").first()
        if not admin_exists:
            admin = User(first_name='Admin', last_name='HBnB', email="admin@hbnb.io", is_admin=True)
            admin.hash_password("admin1234")
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")

        for amenity in amenities:
            amenity_exists = Amenity.query.filter_by(name=amenity["name"]).first()
            if not amenity_exists:
                new_amenity = Amenity(name=amenity["name"])
                db.session.add(new_amenity)
                db.session.commit()