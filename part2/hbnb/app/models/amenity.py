#!/usr/bin/python3
"""This module for the Class Amenity"""


from .base import BaseModel


class Amenity(BaseModel):
    """To create attibutes for the Class"""
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("The name is invalid")
        if not value:
            raise ValueError("The name is required")
        if len(value) > 50:
            raise ValueError("The name is too long")
        self._name = value
