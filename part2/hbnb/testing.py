#!/usr/bin/python3
"""This module tests the User API endpoints"""

import unittest
from app import create_app
import uuid

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
    
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


        print("Status code:", response.status_code)

        self.assertEqual(response.status_code, 201)
        self.owner = response.json


        unique_email = f"test.user.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "ahmed",
            "last_name": "User",
            "email": unique_email
        })


        print("Status code:", response.status_code)

        self.assertEqual(response.status_code, 201)
        self.user = response.json

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
#testing user
    def test_create_user(self):
    
        print("Test de création d'utilisateur en cours...")
        unique_email = f"jane.doe.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
       
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
       
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, 200)

    def test_update_users(self):
       response = self.client.put(f'/api/v1/users/{self.owner["id"]}', json={
        "first_name": "Jane",
        "last_name": "Goe",
        "email": self.owner["email"]
            })
       self.assertEqual(response.status_code, 201)

    def test_update_invalide_users(self):
       response = self.client.put(f'/api/v1/users/{self.owner["id"]}', json={
        "first_name": "Jane",
        "last_name": "Goe",
        "email": self.user["email"]
            })
       self.assertEqual(response.status_code, 400)
#testing Place
    def test_create_place(self):
        
        response = self.client.post('/api/v1/places/', json={
            "title": "Studio",
            "description": "good studio",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -30.4194,
            "owner_id": self.owner["id"],
            "amenities": []
        })

        self.assertEqual(response.status_code, 201)



    def test_create_place_invalid_data(self):
        
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "joulie sudio",
            "price": "",
            "latitude": 37.7749,
            "longitude": -700.4194,  # Valeur hors plage
            "owner_id": self.owner["id"],
            "amenities": []
        })

        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
    
        response = self.client.get('/api/v1/places/')

        self.assertEqual(response.status_code, 200)
#teting review
    def test_create_invalide_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "place_id": self.place["id"],
            "user_id": self.owner["id"],
            "rating": 7,
            "text": "Super endroit!"
            })

        self.assertEqual(response.status_code, 400)



    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "place_id": self.place["id"],
            "user_id": self.user["id"],
            "rating": 5,
            "text": "Super endroit!"
            })

        self.assertEqual(response.status_code, 201)

#test amenity
    def test_create_invalide_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400)

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "picine"
        })

        self.assertEqual(response.status_code, 201)


    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "nfeinof,eo,oifjof,oieo,if,o,fe,iijrnfnfnnufnfuueoeooirijnfzpppzjeo"
        })

        self.assertEqual(response.status_code, 400)
if __name__ == '__main__':
    unittest.main()
