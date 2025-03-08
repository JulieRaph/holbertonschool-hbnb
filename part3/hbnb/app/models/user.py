#!/usr/bin/python3
"""This module for the Class User"""

from app.services.extensions import bcrypt
from .base import BaseModel
import re


class User(BaseModel):
    """To create attibutes for the Class"""
    def __init__(self, first_name, last_name, email, password, is_admin=True):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.hash_password(password)

    def add_place(self, place):
        """This function to add places"""
        self.places.append(place)
        
    def update(self, data):
        if "first_name" in data:
            self.first_name = data["first_name"]
        if "last_name" in data:
            self.last_name = data["last_name"]
        if "email" in data:
            self.email = data["email"]

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
        
    def hash_password(self, password):
        """Hashes the password before storing it."""
        pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not password:
            raise TypeError("Password is required")
        mat = re.search(pattern, password)
        if not mat:
            raise ValueError("Password must have at least: 8 characters, one lowercase letter, one uppercase letter and one special character")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if not value:
            raise TypeError("First name is required")
        if len(value) > 50:
            raise ValueError("First name is too long")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last Name must be a string")
        if not value:
            raise TypeError("Last name is required")
        if len(value) > 50:
            raise ValueError("Last name is too long")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not value:
            raise TypeError("Email is required")
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value
        ):
            raise ValueError("Email is not valid")
        self._email = value
        
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Admin must be True or False")
        self._is_admin = value