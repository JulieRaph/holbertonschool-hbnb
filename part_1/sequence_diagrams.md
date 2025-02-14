# Sequence Diagrams for API Calls

Sequence diagrams for some API calls to illustrate the interaction between the layers (Presentation, Business Logic, Persistence) and the flow of information within the HBnB application.

## User Registration

```mermaid
sequenceDiagram
  participant User as User
  participant UI as UI
  participant API as API
  participant BusinessLogic as BusinessLogic
  participant Database as Database

  User ->> UI: input: fname, lname, email, pass
  UI ->> API: API Call USER create()
  API ->> BusinessLogic: Validate Data and POST Request
  BusinessLogic ->> Database: Save Data
  Database -->> BusinessLogic: Confirm Save
  BusinessLogic -->> API: Return Response
  API -->> UI: Return Success Msg
  UI -->> User: User register success
  alt Register fails
    UI ->> UI: if form fails
    UI -->> User: Display form error msg
    Database ->> Database: if user exits
    Database -->> BusinessLogic: Denied Save
    BusinessLogic -->> API: Return Response
    API -->> UI: Return user exist error msg
    UI -->> User: Display user exit msg
    BusinessLogic ->> BusinessLogic: if server fails
    BusinessLogic -->> API: Return Response
    API -->> UI: Return Server errors msgs
    UI -->> User: Display server error msg
  end
```

## Place Creation

```mermaid
sequenceDiagram
  participant User as User
  participant UI as UI
  participant API as API
  participant BusinessLogic as BusinessLogic
  participant Database as Database

  User ->> UI: input: fname, lname, email, pass
  UI ->> API: API Call PLACE create()
  API ->> BusinessLogic: Validate Data and POST Request
  BusinessLogic ->> Database: Save Data
  Database -->> BusinessLogic: Confirm Save
  BusinessLogic -->> API: Return Response
  API -->> UI: Return Success Msg
  UI -->> User: Place creation success
  alt Place Creation fails
    UI ->> UI: if form fails
    UI -->> User: Display form error msg
    Database ->> Database: if place exits
    Database -->> BusinessLogic: Denied Save
    BusinessLogic -->> API: Return Response
    API -->> UI: Return place exist error msg
    UI -->> User: Display place exit msg
    BusinessLogic ->> BusinessLogic: if server fails
    BusinessLogic -->> API: Return Response
    API -->> UI: Return Server errors msgs
    UI -->> User: Display server error msg
  end
```

## Review Submission

```mermaid
sequenceDiagram
  participant User as User
  participant UI as UI
  participant API as API
  participant BusinessLogic as BusinessLogic
  participant Database as Database

  User ->> UI: input: rating, comments
  UI ->> API: API Call REVIEW create()
  API ->> BusinessLogic: Validate Data and POST Request
  BusinessLogic ->> Database: Save Data
  Database -->> BusinessLogic: Confirm Save
  BusinessLogic -->> API: Return Response
  API -->> UI: Return Success Msg
  UI -->> User: Review creation success
  alt Review Creation fails
    UI ->> UI: if form fails
    UI -->> User: Display form error msg
    BusinessLogic ->> BusinessLogic: if server fails
    BusinessLogic -->> API: Return Response
    API -->> UI: Return Server errors msgs
    UI -->> User: Display server error msg
  end
```

## Fetching a List of Places

```mermaid
sequenceDiagram
  participant User as User
  participant UI as UI
  participant API as API
  participant BusinessLogic as BusinessLogic
  participant Database as Database

  User ->> UI: search places
  UI ->> API: API Call listPlaces()
  API ->> BusinessLogic: Fetch data
  BusinessLogic ->> Database: Request Data
  Database -->> BusinessLogic: Return Data
  BusinessLogic -->> API: Return Response
  API -->> UI: Return Success Msg
  UI -->> User: Display list of places
  alt List places fails
    Database ->> Database: if no places
    Database -->> BusinessLogic: Return empty data
    BusinessLogic -->> API: Return Response
    API -->> UI: Return data not found msg
    UI -->> User: Display places not found
    BusinessLogic ->> BusinessLogic: if server fails
    BusinessLogic -->> API: Return Response
    API -->> UI: Return Server errors msgs
    UI -->> User: Display server error msg
  end
```
