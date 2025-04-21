# holbertonschool-hbnb
This project is a full-stack “HBnB” (Airbnb clone) web application structured around a well-defined three-layer architecture. Here's a detailed analysis of its structure and operation.

## Overall architecture

The project follows a clearly separated three-layer architecture:

1 - Presentation Layer
User interface (HTML/CSS/JS)
API REST (endpoints)

2 - Business Logic Layer
Data models
Business logic

3 - Persistence layer
Database access
Repositories

These layers communicate with each other via the Façade pattern, which provides a simplified interface between the presentation layer and the business layer.

## Project organization

The project is divided into several parts representing the development stages:

* part_1: Documentation and design (class diagrams, sequences)
* part_2: Business logic and API
* part_3: Authentication and database integration
* part_4: Frontend implementation

## Technologies used

BACKEND: 

* Python Flask: Web framework for API
* Flask-RESTx: API documentation via Swagger
* SQLAlchemy: ORM for database management
* Flask-JWT-Extended: Authentication via JWT tokens
* Flask-Bcrypt: Password hashing
* Flask-CORS: Cross-origin query management

FRONTEND:

* HTML/CSS: Web page structure and style
* JavaScript: Dynamic interactions and API communication

## Main components

Data models
Business logic is represented by several main models:

* BaseModel: Base class with common attributes (id, created_at, updated_at)
* User: User management (first_name, last_name, email, password, is_admin)
* Place: Properties for rent (title, description, price, contact details)
* Review : Property reviews (text, rating)
* Amenity: Amenities available (name)

API REST
The API is organized into well-defined namespaces:

* /api/v1/users/ # Managing users
* /api/v1/places/ # Managing properties
* /api/v1/reviews/ # Managing reviews
* /api/v1/amenities/ # Managing equipment
* /api/v1/auth/ # Authentication
* /api/v1/admin/ # Administrative operations

Pattern Façade
The façade (HBnBFacade in app/services/facade.py) is the central component that :

1 - Initializes repositories
2 - Provides simplified methods for all CRUD operations
3 - Acts as intermediary between API and repositories
4 - Handles data validation

Example of its implementation :
python
class HBnBFacade :
 def init(self) :
 self.user_repo = UserRepository()
 self.place_repo = PlaceRepository()
 self.review_repo = ReviewRepository()
 self.amenity_repo = AmenityRepository()

 ## Methods for users, properties, notices, equipment...

 FRONTEND

The frontend is made up of several HTML pages:
* index.html : List of properties with filtering by price
* place.html : Details of a specific property and its notices
* login.html : User authentication
* add_review.html : Notice addition form

JavaScript (scripts.js) manages:
* Authentication (JWT tokens stored in cookies)
* Property retrieval and display
* Property filtering by price
* Form submission

## Interaction flows

Based on sequence diagrams, the main flows are :

1 - User registration:
* The IU collects the data
* The API validates the data
* The business logic creates the user in the database
* The response is returned to the IU

2 - Property creation:
* The IU collects the details
* The API validates the data
* The business logic registers the property
* The response is returned to the IU

3 - Submitting a notification:
* The IU collects the notification data
* The API validates the data
* The business logic registers the notification
* The response is returned to the IU

## Additional features

* JWT-based authentication and authorization
* Data validation in templates and API
* Error handling with appropriate HTTP codes
* Documented manual and unit tests

## CONCLUSION

This project demonstrates a modern web application with a clean architecture, clear separation of concerns and robust design patterns. The facade allows layers to be effectively decoupled, making the application easily maintainable and scalable.
