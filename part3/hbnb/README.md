# HBnB - Project Setup

A brief overview of the project setup

## Project Directory Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## Directories and files

### `app/`

---

Contains the core application code

### `app/api/`

---

Houses the API endpoints, organized by version (v1/).

#### ► Users Api:

* Set up the POST, GET, and PUT endpoints for managing users.
* Implement the logic for handling user-related operations in the Business Logic layer.
* Integrate the Presentation layer (API) and Business Logic layer through the Facade.

``` POST /api/v1/users/ ``` : Registers a new user and performs a check for email uniqueness

``` GET /api/v1/users/<user_id> ``` : Retrieves user details by ID

``` PUT /api/v1/users/<user_id> ``` : Make a partial user modification

#### ► Amenities Api:

* Set up the POST, GET, and PUT endpoints for managing amenities.
* Implement the necessary logic for handling amenity-related operations in the Business Logic layer.
* Integrate the Presentation layer (API) and Business Logic layer through the Facade.

``` POST /api/v1/amenities/ ``` : Register a new amenity

``` GET /api/v1/amenities/ ``` : Retrieve a list of all amenities

``` GET /api/v1/amenities/<amenity_id> ``` : Get amenity details by ID

``` PUT /api/v1/amenities/<amenity_id> ``` : Update an amenity's information

#### ► Places Api:
Given that the Place entity has relationships with other entities, such as User (owner) and Amenity, you’ll need to handle these relationships carefully while maintaining the integrity of the application logic.

* Set up the POST, GET, and PUT endpoints for managing places.
* Implement the logic for handling place-related operations in the Business Logic layer.
* Integrate the Presentation layer (API) and Business Logic layer through the Facade.
* Implement validation for specific attributes like price, latitude, and longitude.
* Ensure that related data such as owner details and amenities are properly handled and returned with the Place data.

``` POST /api/v1/places/ ``` : Register a new place

``` GET /api/v1/places/ ``` : Return a list of all places

``` GET /api/v1/places/<place_id> ``` : Retrieve details of a specific place, including its associated owner and amenities

``` PUT /api/v1/places/<place_id> ``` : Update place information

#### ► Reviews Api:

* Set up the POST, GET, PUT, and DELETE endpoints for managing reviews.
* Implement the logic for handling review-related operations in the Business Logic layer.
* Integrate the Presentation layer (API) and Business Logic layer through the Facade.
* Implement validation for specific attributes like the text and rating of the review, and ensure that the review is associated with both a user and a place.
* Update the Place model in api/v1/places.py to consider the collection of reviews for a place

``` POST /api/v1/reviews/ ``` : Register a new review

``` GET /api/v1/reviews/ ``` : Return a list of all reviews

``` GET /api/v1/reviews/<review_id> ``` : Retrieve details of a specific review

``` GET /api/v1/places/<place_id>/reviews ``` : Retrieve all reviews for a specific place

``` PUT /api/v1/reviews/<review_id> ``` : Update a review’s information

``` DELETE /api/v1/reviews/<review_id>``` : Delete a review

### `app/models/`

---

Contains the Business Logic Classes

#### ► class BaseModel:

Attributes:

- id(UUID4): Unique identifier for each user.
- created_at (DateTime): Timestamp when the user is created.
- updated_at (DateTime): Timestamp when the user is last updated.

Methods:

- save(): Update the updated_at timestamp whenever the object is modified.
- update(): Update the attributes of the object based on the provided dictionary.

#### ► class User(BaseModel):

Attributes:

- first_name (String): The first name of the user. Required, maximum length of 50 characters.
- last_name (String): The last name of the user. Required, maximum length of 50 characters.
- email (String): The email address of the user. Required, must be unique, and should follow standard email format validation.
- is_admin (Boolean): Indicates whether the user has administrative privileges. Defaults to False.

#### ► class Place(BaseModel):

Attributes:

- title (String): The title of the place. Required, maximum length of 100 characters.
- description (String): Detailed description of the place. Optional.
- price (Float): The price per night for the place. Must be a positive value.
- latitude (Float): Latitude coordinate for the place location. Must be within the range of -90.0 to 90.0.
- longitude (Float): Longitude coordinate for the place location. Must be within the range of -180.0 to 180.0.
- owner (User): User instance of who owns the place. This should be validated to ensure the owner exists.

Methods:

- add_review(): Add a review to the place.
- add_amenity(): Add an amenity to the place.

#### ► class Review(BaseModel):

Attributes:

- text (String): The content of the review. Required.
- rating (Integer): Rating given to the place, must be between 1 and 5.
- place (Place): Place instance being reviewed. Must be validated to ensure the place exists.
- user (User): User instance of who wrote the review. Must be validated to ensure the user exists.

#### ► class Amenity(BaseModel):

Attributes:

- name (String): The name of the amenity (e.g., "Wi-Fi", "Parking"). Required, maximum length of 50 characters.

### `app/services/`

---

Where the Facade pattern is implemented, managing the interaction between layers.

### `app/persistence/`

---

Where the in-memory repository is implemented for testing purpouse before the implementation of a database-backed solution using SQL Alchemy.

### `run.py`

---

The entry point for running the Flask application.

### `config.py`

---

Used for configuring environment variables and application settings.

### `requirements.txt`

---

List all the Python packages needed for the project.

### `testing.py`

---

Implement testing and validation of the Endpoints.

Implement basic validation checks for each of the attributes in your endpoints.


* Perform black-box testing using cURL and the Swagger documentation generated by Flask-RESTx.

#### Testing the Creation of a User using cURL
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'
```

**Expected Response:**

```jsonc
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}

// 200 OK
```

#### Testing Invalid Data for a User using cURL
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'
```

**Expected Response:**

```json
{
    "error": "Invalid input data"
}

// 400 Bad Request
```

#### Testing the Creation of a place using Swagger

`POST`/api/v1/places/  (Register a new place)
```
{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "amenities": [
    "1fa85f64-5717-4562-b3fc-2c963f66afa6"
  ]
}
```
**Expected Status:**

`201`  Place successfully created

`400`  Invalid input data

#### Testing the update a place's information using Swagger

`PUT`/api/v1/places/{place_id} (Update a place's information)
```
{
  "title": "Super Apartment",
  "description": "A super place for your week-end!",
  "price": 150,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "amenities": [
    "1fa85f64-5717-4562-b3fc-2c963f66afa6"
  ]
}
```
**Expected Status:**

`200`  	Place updated successfully

`400`   Invalid input data

`404`   Place not found




* Create a detailed testing report, highlighting both successful and failed cases.

In addition to manual tests, you should write automated unit tests using Python’s `unittest` or `pytest` frameworks. 

Here’s a basic example of how to structure your tests:
```python
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
```


### `README.md`

---

A brief overview of the project.

## Installing dependencies and running the application

#### 1. Install Required Packages

As in the `requirements.txt` file are the list of Python packages needed for the project, install dependencies using:

```
pip install -r requirements.txt
```

#### 2. Run the application

```
python run.py
```
