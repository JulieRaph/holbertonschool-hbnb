#!/usr/bin/python3
"""This module for the Class Amenity"""

from app import db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """To create attibutes for the Class"""
    __tablename__ = 'amenity'

    name = db.Column(db.String(50), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    place = db.relationship('Place', backref='amenities', lazy=True)

    @validates('name')
    def validates_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Name is invalid")
        if not value:
            raise ValueError("Name is required")
        if len(value) > 50:
            raise ValueError("Name is too long")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
