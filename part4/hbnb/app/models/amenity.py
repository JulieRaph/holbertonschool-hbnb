#!/usr/bin/python3
"""This module for the Class Amenity"""
from app import db
import uuid
from .base import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """To create attibutes for the Class"""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    
    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Name is invalid")
        if len(value.replace(" ", "")) < 2 or len(value.replace(" ", "")) > 50:
            raise ValueError("Name must have between 2 and 50 characters")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
