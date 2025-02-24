#!/usr/bin/python3
"""This module for the Class Review"""


from .base import BaseModel


class Review(BaseModel):
    """To create attibutes for the Class"""
    def __init__(self, place, user, rating, text):
        super().__init__()
        self.place = place
        self.user = user
        self.rating = rating
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("The text is invalid")
        if not value:
            raise ValueError("The text is required")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not value:
            raise ValueError("The rating is required")
        if value < 1 or value > 5:
            raise ValueError("The rating must be between 1 and 5")
        if not isinstance(value, int):
            raise TypeError("The rating is invalid")
        self._rating = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not value:
            raise ValueError("The place is required")
        self._place = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not value:
            raise ValueError("The user is required")
        self._user = value
