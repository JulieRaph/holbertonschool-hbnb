import os
import random
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.associations import place_amenity
from sqlalchemy import insert 
from app import db
from flask import current_app

amenities = [
    {"name": "WiFi"},
    {"name": "Swimming Pool"},
    {"name": "Air Conditioning"},
    {"name": "Parking"}
]

users = [
    {"first_name": "Jane", "last_name": "Doe", "email": "jane@email.com", "password": "jane1234", "role": "owner"},
    {"first_name": "Peter", "last_name": "Parker", "email": "spiderman@email.com", "password": "peter1234", "role": "owner"},
    {"first_name": "Pierre", "last_name": "Dubois", "email": "pierre@email.com", "password": "pierre1234", "role": "owner"},
    {"first_name": "John", "last_name": "Doe", "email": "john@email.com", "password": "john1234", "role": "user"},
    {"first_name": "Matthieu", "last_name": "Dupont", "email": "matthieu@email.com", "password": "matthieu1234", "role": "user"},
    {"first_name": "Sophie", "last_name": "Martin", "email": "sophie@email.com", "password": "sophie1234", "role": "user"},
]

places = [
    {"title": "Seaside Serenity Cottage", "description": "Relax in our charming seaside cottage with stunning ocean views and tranquil sunsets. Perfect for a peaceful getaway.", "price": random.randint(5,150), "latitude": random.uniform(-90.0, 90.0), "longitude": random.uniform(-180.0, 180.0)},
    {"title": "Urban Loft with City Skyline Views", "description": "Modern downtown loft with incredible city skyline views. Enjoy easy access to cafes, galleries, and nightlife.", "price": random.randint(5,150), "latitude": random.uniform(-90.0, 90.0), "longitude": random.uniform(-180.0, 180.0)},
    {"title": "Mountain Retreat Cabin", "description": "Cozy, secluded mountain cabin surrounded by pines. Ideal for hiking and enjoying nature's quiet.", "price": random.randint(5,150), "latitude": random.uniform(-90.0, 90.0), "longitude": random.uniform(-180.0, 180.0)},
    {"title": "Historic Townhouse in Old Quarter", "description": "Restored townhouse in the charming old quarter. Explore cobblestone streets and rich history.", "price": random.randint(5,150), "latitude": random.uniform(-90.0, 90.0), "longitude": random.uniform(-180.0, 180.0)},
    {"title": "Tropical Paradise Bungalow", "description": "Secluded island bungalow with white sand beaches and clear waters. Perfect for a tropical escape.", "price": random.randint(5,150), "latitude": random.uniform(-90.0, 90.0), "longitude": random.uniform(-180.0, 180.0)},
    {"title": "Rustic Farmhouse Getaway", "description": "Peaceful country farmhouse surrounded by rolling hills. Enjoy the simple pleasures of rural life.", "price": random.randint(5,150), "latitude": random.uniform(-90.0, 90.0), "longitude": random.uniform(-180.0, 180.0)},
]

reviews = [
    {"rating": 4, "text": "A solid choice for a comfortable stay. The location was good, and the overall experience was positive. I'd recommend it."},
    {"rating": 5, "text": "Truly a wonderful experience. Everything was excellent, and the atmosphere was perfect. I thoroughly enjoyed my time here."},
    {"rating": 3, "text": "It was adequate for my needs. The location was convenient, and the place was acceptable. Nothing particularly stood out, but nothing was bad."},
    {"rating": 5, "text": "An exceptional stay! The atmosphere was welcoming, and the overall experience was fantastic. I'd happily return."},
    {"rating": 4, "text": "A pleasant experience. The place was clean and comfortable, and the surroundings were nice. I was satisfied with my stay."},
    {"rating": 3, "text": "It was an okay stay. It served its purpose, but it wasn't anything special. It was fine for a short trip."},
]


def db_populate():
    with current_app.app_context():
        # Populate Amenitites
        for amenity in amenities:
            amenity_exists = Amenity.query.filter_by(name=amenity['name']).first()
            if not amenity_exists:
                new_amenity = Amenity(name=amenity['name'])
                db.session.add(new_amenity)
                db.session.commit()
                created_amenity = Amenity.query.filter_by(name=amenity['name']).first()
                amenity['id'] = created_amenity.id
        # Populate Users
        for user in users:
            user_exists = User.query.filter_by(email=user["email"]).first()
            if not user_exists:
                new_user = User(first_name=user["first_name"], last_name=user["last_name"], email=user["email"])
                new_user.hash_password(user["password"])
                db.session.add(new_user)
                db.session.commit()
                created_user = User.query.filter_by(email=user["email"]).first()
                user["id"] = created_user.id
        # Populate Places
        owners = [user for user in users if user["role"] == "owner"]
        idx_user = 0
        idx_amenity = 0
        for place in places:
            place_exists = Place.query.filter_by(title=place["title"]).first()
            if not place_exists:
                new_place = Place(title=place["title"], description=place["description"], price=place["price"], latitude=place["latitude"], longitude=place["longitude"], owner_id=owners[idx_user]["id"])
                db.session.add(new_place)
                db.session.commit()
                created_place = Place.query.filter_by(title=place["title"]).first()
                db.session.execute(
                    insert(place_amenity).values([
                        {"place_id": created_place.id, "amenity_id": amenities[idx_amenity]["id"]},
                        {"place_id": created_place.id, "amenity_id": amenities[idx_amenity + 1]["id"]}
                    ])
                )
                db.session.commit()
                place["id"] = created_place.id
                idx_user = idx_user + 1 if idx_user <= 1 else 0
                idx_amenity = idx_amenity + 1 if idx_amenity <= 1 else 0
        # Populate Reviews        
        not_owners = [user for user in users if user["role"] == "user"]
        idx_place = 3
        for review in reviews:
            review_exists = Review.query.filter_by(text=review["text"]).first()
            if not review_exists:
                new_review = Review(rating=review["rating"], text=review["text"], place_id=places[idx_place]["id"], user_id=not_owners[idx_user]["id"])
                db.session.add(new_review)
                db.session.commit()
                idx_place = idx_place + 1 if idx_place <= 2 else 0
                idx_user = idx_user + 1 if idx_user <= 1 else 0