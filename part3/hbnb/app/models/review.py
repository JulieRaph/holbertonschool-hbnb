#!/usr/bin/python3
"""This module for the Class Review"""
from app import db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    """To create attibutes for the Class"""
    __tablename__ = 'review'

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)

    place = db.relationship('Place', backref='reviews', lazy=True)
    user = db.relationship('User', backref='reviews', lazy=True)

    def update(self, data):
        if 'text' in data:
            self.text = data['text']
        if 'rating' in data:
            self.rating = data['rating']

    @validates('text')
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text is not valid")
        if not value:
            raise TypeError("Text is required")
        return value


    @validates('rating')
    def rating(self, value):
        if not value:
            raise TypeError("Rating is required")
        if not isinstance(value, int):
            raise TypeError("Rating is not valid")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value


    @validates('place_id')
    def place_id(self, value):
        if not value:
            raise TypeError("Place is required")
        if not isinstance(value, str):
            raise TypeError("Place is not valid")
        return value

    @validates('user_id')
    def user_id(self, value):
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
