# Sequence Diagrams for API Calls

Sequence diagrams for some API calls to illustrate the interaction between the layers (Presentation, Business Logic, Persistence) and the flow of information within the HBnB application.

## User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call USER create()
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Save Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API -->> User: Display Success Msg
API -->> User: Display form error msg
API -->> User: Display user exist error msg
API -->> User: Server errors msgs
```

## Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call PLACE Create()
API->>BusinessLogic: Validate Data and POST Request
BusinessLogic->>Database: Save Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API -->> User: Display Success Msg
API -->> User: Display form error msg
API -->> User: Display place exist error msg
API -->> User: Server errors msgs
```

## Review Submission

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call REVIEW Create()
API->>BusinessLogic: Validate Data and POST Request
BusinessLogic->>Database: Save Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API -->> User: Display Success Msg
API -->> User: Display form error msg
API -->> User: Server errors msgs
```

## Fetching a List of Places

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call REVIEW Create()
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Save Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API -->> User: Display Success Msg
API -->> User: Display form error msg
```
