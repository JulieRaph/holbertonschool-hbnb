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

#### `app/`

Contains the core application code

#### `app/api/`

Houses the API endpoints, organized by version (v1/).

#### `app/models/`

Contains the business logic classes (e.g., user.py, place.py).

#### `app/services/`

Where the Facade pattern is implemented, managing the interaction between layers.

#### `app/persistence/`

Where the in-memory repository is implemented for testing purpouse before the implementation of a database-backed solution using SQL Alchemy.

#### `run.py`

The entry point for running the Flask application.

#### `config.py`

Used for configuring environment variables and application settings.

#### `requirements.txt`

List all the Python packages needed for the project.

#### `README.md`

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
