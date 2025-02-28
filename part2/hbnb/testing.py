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

        #Création d'un amenity test pour place
        response_amenity = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })

        print("Création d'un amenity test...")
        print("Status code:", response_amenity.status_code)

        self.assertEqual(response_amenity.status_code, 201)
        self.amenity = response_amenity.json

        #Création d'un amenity test pour place
        response_amenity = self.client.post('/api/v1/amenities/', json={
            "name": "Douche"
        })

        print("Création d'un amenity test...")
        print("Status code:", response_amenity.status_code)

        self.assertEqual(response_amenity.status_code, 201)
        self.amenity2 = response_amenity.json


        #Creation d'un review 
        response_review = self.client.post('/api/v1/reviews/', json={
            "text": "Super cool!",
            "rating": 5,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })

        print("Création d'un review test...")
        print("Status code:", response_review.status_code)

        self.assertEqual(response_review.status_code, 201)
        self.review = response_review.json

#testing user
#create user
#success example
    def test_create_user(self):
    
        print("Test de création d'utilisateur en cours...")
        unique_email = f"jane.doe.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 201)
#create user
#unsuccess examples
    def test_create_user_invalid_data(self):
       
        print("Test de création d'utilisateur en cours...")
        unique_email = f"jane.doe.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/users/', json={
            "first_name": "azertyuiopmlkjhgfdsqwxcvbnpoiuuyttrtzrasaswvzjcnvbdjglbkcnsjqkckvnfnvgjgtbzvchxqidodvvnbddfhvbvncfghj",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "fhrjtgu"
        })
        self.assertEqual(response.status_code, 400)

#get user
#success example
    def test_get_users(self):
       
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, 200)

    def test_get_users_by_id(self):

        response = self.client.get(f'/api/v1/users/{self.user["id"]}')

        self.assertEqual(response.status_code, 200)

#get user
#unsuccess example
    def test_get_users_no_id(self):

        response = self.client.get('/api/v1/users/256321478596')

        self.assertEqual(response.status_code, 404)

#update user
#success example
    def test_update_users(self):
       response = self.client.put(f'/api/v1/users/{self.owner["id"]}', json={
        "first_name": "Jane",
        "last_name": "Goe",
        "email": self.owner["email"]
            })
       self.assertEqual(response.status_code, 201)

#update user
#unsuccess examples
    def test_update_invalide_users(self):
       response = self.client.put(f'/api/v1/users/{self.owner["id"]}', json={
        "first_name": "Jane",
        "last_name": "Goe",
        "email": self.user["email"]
            })
       self.assertEqual(response.status_code, 400)
    
    def test_update_users_not_found(self):
        response = self.client.put(f'/api/v1/users/gutyrhfbdvcjeoisplcdk', json={
        "first_name": "Jane",
        "last_name": "Goe",
        "email": self.owner["email"]
            })
        self.assertEqual(response.status_code, 404)

#testing Place
#create place
#success example
    def test_create_place(self):
        
        response = self.client.post('/api/v1/places/', json={
            "title": "Studio",
            "description": "good studio",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -30.4194,
            "owner_id": self.owner["id"],
            "amenities": [self.amenity["id"]]
        })

        self.assertEqual(response.status_code, 201)

#unsuccess example
    def test_create_place_invalid_data(self):
        
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "joulie sudio",
            "price": 200,
            "latitude": 37.7749,
            "longitude": 80.4194,  # Valeur hors plage
            "owner_id": self.owner["id"],
            "amenities": [self.amenity["id"]]
        })

        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "joulie sudio",
            "price": -10,
            "latitude": 37.7749,
            "longitude": 80.4194,  # Valeur hors plage
            "owner_id": self.owner["id"],
            "amenities": [self.amenity["id"]]
        })

        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "joulie sudio",
            "price": -10,
            "latitude": 37.7749,
            "longitude": 80.4194,  # Valeur hors plage
            "owner_id": self.owner["id"],
            "amenities": ["ljkd556csvgb"]
        })

        self.assertEqual(response.status_code, 400)

#get place
#success example
    def test_get_places(self):
    
        response = self.client.get('/api/v1/places/')

        self.assertEqual(response.status_code, 200)

    def test_get_places_by_id(self):

        response = self.client.get(f'/api/v1/places/{self.place["id"]}')

        self.assertEqual(response.status_code, 200)

#unsuccess example

    def test_get_places_not_found(self):

        response = self.client.get(f'/api/v1/places/gjthlnkvhsbzhcjr52363')

        self.assertEqual(response.status_code, 404)

#put place
#success example

    def test_put_place(self):

        response = self.client.put(f'/api/v1/places/{self.place["id"]}', json={
            "title": "Studio",
            "description": "super studio",
            "price": 500,
            "latitude": 37.7749,
            "longitude": -30.4194,
            "owner_id": self.owner["id"],
            "amenities": [self.amenity["id"]]
        })

        self.assertEqual(response.status_code, 200)

#unsuccess examples

    def test_put_places_not_found(self):

        response = self.client.put('/api/v1/places/hjfbvs621s41vbd6fsf', json={
            "title": "Studio",
            "description": "super studio",
            "price": 500,
            "latitude": 37.7749,
            "longitude": -30.4194,
            "owner_id": self.owner["id"],
            "amenities": [self.amenity["id"]]
        })

        self.assertEqual(response.status_code, 404)

    def test_put_invalid_data(self):

        response = self.client.put(f'/api/v1/places/{self.place["id"]}', json={
            "title": "Studio",
            "description": "super studio",
            "price": 500,
            "latitude": 526.56,
            "longitude": -30.4194,
            "owner_id": self.owner["id"],
            "amenities": [self.amenity["id"]]
        })

        self.assertEqual(response.status_code, 400)
        
#testing review
#create review
#success example
        
    def test_create_review(self):

        response = self.client.post('/api/v1/reviews/', json={
            "place_id": self.place["id"],
            "user_id": self.user["id"],
            "rating": 5,
            "text": "Super endroit!"
        })

        self.assertEqual(response.status_code, 201)

#unsuccess
    def test_create_invalid_review(self):

        response = self.client.post('/api/v1/reviews/', json={
            "place_id": self.place["id"],
            "user_id": self.owner["id"],
            "rating": 7,
            "text": "Super endroit!"
            })

        self.assertEqual(response.status_code, 400)

#get review
#success example

    def test_get_review(self):

        response = self.client.get('/api/v1/reviews/')

        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id(self):

        response = self.client.get(f'/api/v1/reviews/{self.review["id"]}')

        self.assertEqual(response.status_code, 200)

    def test_get_by_place_id(self):

        response = self.client.get(f'/api/v1/reviews/places/{self.place["id"]}/reviews')

        self.assertEqual(response.status_code, 200)

#unsuccess examples

    def test_get_place_review_not_found(self):

        response = self.client.get(f'/api/v1/reviews/places/fheqjqslvldbfksxnqsndcn/reviews')

        self.assertEqual(response.status_code, 404)

    def test_get_review_not_found(self):

        response = self.client.get('/api/v1/reviews/id')

        self.assertEqual(response.status_code, 404)

#put review
#success example

    def test_put_review(self):

        response = self.client.put(f'/api/v1/reviews/{self.review["id"]}', json={
            "text": "Not so cool!",
            "rating": 3,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })

        self.assertEqual(response.status_code, 200)

#unsuccess examples

    def test_put_review_not_found(self):

        response = self.client.put('/api/v1/reviews/gjtiflkszncknv/')

        self.assertEqual(response.status_code, 404)

    def test_put_review_invalid_data(self):

        response = self.client.put(f'/api/v1/reviews/{self.review["id"]}', json={
            "text": "Not so cool!",
            "rating": 14,
            "user_id": self.user["id"],
            "place_id": self.place["id"]
        })

        self.assertEqual(response.status_code, 400)

#delete review
#success example

    def test_delete_review(self):

        response = self.client.put(f'/api/v1/reviews/{self.review["id"]}')

        self.assertEqual(response.status_code, 200)

#unsuccess example

    def test_delete_not_found(self):

        response = self.client.put('/api/v1/reviews/azerty')

        self.assertEqual(response.status_code, 404)

#test amenity
#create amenity
#success example

    def test_create_amenity(self):

        response = self.client.post('/api/v1/amenities/', json={
            "name": "piscine"
        })

        self.assertEqual(response.status_code, 201)

#unsuccess examples

    def test_create_amenity_invalid_data(self):

        response = self.client.post('/api/v1/amenities/', json={
            "name": "nfeinof,eo,oifjof,oieo,if,o,fe,iijrnfnfnnufnfuueoeooirijnfzpppzjeo"
        })

        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400)

#get amenity
#success examples

    def test_get_amenity(self):

        response = self.client.get('/api/v1/amenities/')

        self.assertEqual(response.status_code, 200)

    def test_get_amenity_by_id(self):

        response = self.client.get(f'/api/v1/amenities/{self.amenity["id"]}')

        self.assertEqual(response.status_code, 200)

#unsuccess

    def test_get_amenity_by_id_not_found(self):

        response = self.client.get('/api/v1/amenities/idfgtre')

        self.assertEqual(response.status_code, 404)

#put amenity
#success example

    def test_put_amenity(self):

        response = self.client.put(f'/api/v1/amenities/{self.amenity["id"]}', json={
            "name": "Garage"
        })

        self.assertEqual(response.status_code, 201)

#unsuccess examples

    def test_put_amenity_invalid_data(self):

        response = self.client.put(f'/api/v1/amenities/{self.amenity2["id"]}', json={
            "name": "Wi-Fi"
        })

        self.assertEqual(response.status_code, 400)

    def test_put_amenity_not_found(self):

        response = self.client.put('/api/v1/amenities/gjhlsjnz/', json={
            "name": "Wi-Fi"
        })

        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
