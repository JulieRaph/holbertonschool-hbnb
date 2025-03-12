#!/usr/bin/python3
"""This module for the Class Review"""
from app import db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    """To create attibutes for the Class"""
    __tablename__ = 'reviews'

    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    places = db.relationship('Place', secondary=db.places_reviews, lazy='subquery',
                              backref=db.backref('reviews', lazy=True))

    def update(self, data):
        if 'text' in data:
            self.text = data['text']
        if 'rating' in data:
            self.rating = data['rating']

    @validates('text')
    def validates_text(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Text is not valid")
        if not value:
            raise TypeError("Text is required")
        return value


    @validates('rating')
    def validates_rating(self, key, value):
        if not value:
            raise TypeError("Rating is required")
        if not isinstance(value, int):
            raise TypeError("Rating is not valid")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value


    @validates('place_id')
    def validates_place_id(self, key, value):
        if not value:
            raise TypeError("Place is required")
        if not isinstance(value, str):
            raise TypeError("Place is not valid")
        return value

    @validates('user_id')
    def validates_user_id(self, key, value):
        if not value:
            raise TypeError("User is required")
        if not isinstance(value, str):
            raise TypeError("User is not valid")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
