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
---------------------

Contains the core application code

### `app/api/`
---------------------

Houses the API endpoints, organized by version (v1/).

### `app/models/`
---------------------

Contains the Business Logic Classes

#### class BaseModel:

Attributes:
* id(UUID4): Unique identifier for each user.
* created_at (DateTime): Timestamp when the user is created.
* updated_at (DateTime): Timestamp when the user is last updated.

Methods:
* save(): Update the updated_at timestamp whenever the object is modified.
* update(): Update the attributes of the object based on the provided dictionary.


#### class User(BaseModel):

Attributes:
* first_name (String): The first name of the user. Required, maximum length of 50 characters.
* last_name (String): The last name of the user. Required, maximum length of 50 characters.
* email (String): The email address of the user. Required, must be unique, and should follow standard email format validation.
* is_admin (Boolean): Indicates whether the user has administrative privileges. Defaults to False.


#### class Place(BaseModel):

Attributes:
* title (String): The title of the place. Required, maximum length of 100 characters.
* description (String): Detailed description of the place. Optional.
* price (Float): The price per night for the place. Must be a positive value.
* latitude (Float): Latitude coordinate for the place location. Must be within the range of -90.0 to 90.0.
* longitude (Float): Longitude coordinate for the place location. Must be within the range of -180.0 to 180.0.
* owner (User): User instance of who owns the place. This should be validated to ensure the owner exists.

Methods:
* add_review(): Add a review to the place.
* add_amenity(): Add an amenity to the place.


#### class Review(BaseModel):

Attributes:
* text (String): The content of the review. Required.
* rating (Integer): Rating given to the place, must be between 1 and 5.
* place (Place): Place instance being reviewed. Must be validated to ensure the place exists.
* user (User): User instance of who wrote the review. Must be validated to ensure the user exists.


#### class Amenity(BaseModel):

Attributes:
* name (String): The name of the amenity (e.g., "Wi-Fi", "Parking"). Required, maximum length of 50 characters.


### `app/services/`
---------------------

Where the Facade pattern is implemented, managing the interaction between layers.

### `app/persistence/`
---------------------

Where the in-memory repository is implemented for testing purpouse before the implementation of a database-backed solution using SQL Alchemy.

### `run.py`
---------------------

The entry point for running the Flask application.

### `config.py`
---------------------

Used for configuring environment variables and application settings.

### `requirements.txt`
---------------------

List all the Python packages needed for the project.

### `README.md`
---------------------

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

