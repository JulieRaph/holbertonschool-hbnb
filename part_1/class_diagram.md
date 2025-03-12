# Class Diagram for Business Logic Layer

A detailed class diagram for the Business Logic layer of the HBnB application. This diagram depicts the entities within this layer, their attributes, methods, and the relationships between them.

```mermaid
classDiagram
class User {
    +String ID
    +String firstName
    +String lastName
    +String email
    +String password
    +Boolean isAdmin
    +Int createdAt
    +Int updatedAt
    +create()
    +read()
    +update()
    +delete()
}
class Place {
    +String ID
    +String owner
    +String title
    +String description
    +Obj Address
    +Array amenities
    +Int price
    +Int latitude
    +Int longitud
    +Int createdAt
    +Int updatedAt
    +create()
    +read()
    +update()
    +delete()
}
class Review {
    +String ID
    +String place
    +String user
    +Int rating
    +String comment
    +Int createdAt
    +Int updatedAt
    +create()
    +read()
    +delete()
}
class Amenity {
    +String ID
    +String name
    +String description
    +Int createdAt
    +Int updatedAt
    +create()
    +read()
    +update()
    +delete()
}
Place --* User : Composition
Review --* Place : Composition
Amenity --> Place: Association
User --o Place : Aggregation
User --o Review : Aggregation
```

## Explanatory Notes

## Entities

### User Entity

Each user has a first name, last name, email, and password
Users should be able to register (user), update (user) their profile information, and be deleted (user/admin).

### Place Entity

Each place has a title, description, price, latitude, and longitude.
Places are associated with the user who created them.
Places can have a list of amenities
Places can be created (user), updated (user), deleted (user/admin), and listed (user/admin).

### Review Entity

Each review is associated with a specific place and user, and includes a rating and comment.
Reviews can be created (user), deleted (user/admin), and listed (user/admin) by place.

### Amenity Entity

Each amenity has a name, and description.
Amenities can be created (admin), updated (admin), deleted (admin), and listed (user/admin).

## Relationships

### Association ( –> )

Represents a bi-directional relationship between two classes.
It establishes a connection between objects of the two classes.
In this diagram each place could have a list of amenities

### Aggregation ( o– )

Represents a “whole-part” relationship.
It’s a weaker form of association where one class (the whole) contains objects of another class (the part), but the part can exist independently of the whole.
In this diagram each place should have an owner and each review should be written by a user

### Composition ( \*– )

A stronger form of aggregation.
Represents a “whole-part” relationship where the part cannot exist without the whole. If the whole is destroyed, the part is destroyed as well.
In this diagram if a user is deleted the place that he/she owns is deleted and if a place is deleted all its reviews are deleted
