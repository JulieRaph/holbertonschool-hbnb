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
    +update()
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
