#!/usr/bin/python3
"""This module for the Class Place"""

from app import db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates


class Place(BaseModel):
    """To create attibutes for the Class"""
    __tablename__ = 'place'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amenities = db.relationship('Amenity', backref='place', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True)
        
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    # def add_amenity(self, amenity):
    #     """Add an amenity to the place."""
    #     self.amenities.append(amenity)

    def remove_review(self, review):
        """Remove a review to the place"""
        self.reviews.remove(review)
        
    def update(self, data):
        if "title" in data:
            self.title = data["title"]
        if "description" in data:
            self.description = data["description"]
        if "price" in data:
            self.price = data["price"]
        if "latitude" in data:
            self.latitude = data["latitude"]
        if "longitude" in data:
            self.longitude = data["longitude"]
        if "amenities" in data:
            self.amenities = data["amenities"]
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": self.amenities,
            "reviews": self.reviews
        }

    @validates('title')
    def validates_title(self, key, value):
        if not value:
            raise TypeError("Title is required")
        if not isinstance(value, str):
            raise TypeError("Title value is not valid")
        if len(value) > 100:
            raise ValueError("Title is too long")
        return value

    @validates('description')
    def validates_description(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Description value is not valid")
        return value

    @validates('price')
    def validates_price(self, key, value):
        if not value:
            raise TypeError("Price is required")
        if not isinstance(value, (float, int)):
            raise TypeError("Price value is not valid")
        if value < 0:
            raise ValueError("Price must be a positive number")
        return value


    @validates('latitude')
    def validates_latitude(self, key, value):
        if not value:
            raise TypeError("Latitude is required")
        if not isinstance(value, float):
            raise TypeError("Latitude is not valid")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value


    @validates('longitude')
    def validates_longitude(self, key, value):
        if not value:
            raise TypeError("Longitude is required")
        if not isinstance(value, float):
            raise TypeError("Longitude is not valid")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

 

    @validates('owner_id')
    def validates_owner_id(self, key, value):
        if not value:
            raise TypeError("Owner ID is required")
        if not isinstance(value, str):
            raise TypeError("Owner ID is not valid")
        return value
