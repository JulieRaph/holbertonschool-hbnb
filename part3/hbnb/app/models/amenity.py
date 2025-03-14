#!/usr/bin/python3
"""This module for the Class Amenity"""
from app import db
import uuid
from .base import BaseModel
from .associations import place_amenity
from sqlalchemy.orm import validates, relationship


class Amenity(BaseModel):
    """To create attibutes for the Class"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
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
