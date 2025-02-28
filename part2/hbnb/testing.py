#!/usr/bin/python3
"""This module tests the User API endpoints"""

import unittest
from app import create_app
import uuid

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the test client before each test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Création d'un utilisateur test avec un email unique
        unique_email = f"test.user.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": unique_email
        })

        print("Création de l'utilisateur test avec email:", unique_email)
        print("Status code:", response.status_code)

        self.assertEqual(response.status_code, 201)
        self.owner = response.json

        # Création d'un lieu test pour les reviews
        response_place = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 50,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner["id"],
            "amenities": []
        })

        print("Création du lieu test...")
        print("Status code:", response_place.status_code)

        self.assertEqual(response_place.status_code, 201)  # Vérifie la création du lieu
        self.place = response_place.json

    def test_create_user(self):
        """Test user creation with valid data"""
        print("Test de création d'utilisateur en cours...")
        unique_email = f"jane.doe.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email
        })
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_place_invalid_data(self):
        """Test de création d'un lieu avec des données invalides"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "Invalid place",
            "price": "",
            "latitude": 37.7749,
            "longitude": -700.4194,  # Valeur hors plage
            "owner_id": self.owner["id"],
            "amenities": []
        })
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/')
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_invalide_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "place_id": self.place["id"],
            "user_id": self.owner["id"],
            "rating": 7,
            "text": "Super endroit!"
            })
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 400)



    def test_create_invalide_aminity(self):
        response = self.client.post('/api/v1/aminities/', json={
            "name": "olsc,pùmw;ùd:QS%M^;zd;md:plodoldl"
        })
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
