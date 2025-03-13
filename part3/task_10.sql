-- SQL Scripts for Table Creation
CREATE DATABASE hbnb_db;
USE hbnb_db;


-- create table User
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);


-- create table Place
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36), 
    Foreign key (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- create table Review
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
    text TEXT NOT NULL,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    Foreign key(user_id) REFERENCES User(id) ON DELETE CASCADE,
    Foreign key(place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id)
);

-- create table Amenity
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY NOT NULL DEFAULT (UUID()),
    name VARCHAR(255) UNIQUE
);

-- create table Place_Amenity
CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    Foreign key(place_id) REFERENCES Place(id) ON DELETE CASCADE,
    Foreign key(amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE,
    primary key (place_id, amenity_id)
);


-- Insert user data
INSERT INTO User (id, email, first_name, last_name,  password, is_admin) VALUES
    ('36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$Hv7Pl9kTapzDfZtNr9FFhuWVgRszzcSh88B9mEejekFsAqPX2Pd8S',
    True
);

-- Insert Amenity data
INSERT INTO Amenity (id, name) VALUES
    ('10de2dac-d19f-4f6a-a07d-91ed34b97c57', 'WiFi'),
    ('fd58d22b-c846-4e87-993a-9b4e5ec6eb83', 'Swimming Pool'),
    ('c145807b-9134-4283-8f97-8025dbd2f997', 'Air Conditioning');


-- Insert User data
INSERT INTO User (id, email, first_name, last_name, password, is_admin) 
VALUES ('d9e39b5b-b8e5-4f6d-a16d-0d6c23c8a7df', 'user@hbnb.io', 'John', 'Doe', '$2b$12$Hv7Pl9kTapzDfZtNr9FFhuWVgRszzcSh88B9mEejekFsAqPX2Pd8S', FALSE);

-- Inset Place data
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id) 
VALUES ('c55d8d7d-cf02-48ed-a97f-9d8a1c87d5a7', 'Beautiful Villa', 'A stunning villa in the hills', 250.00, 40.748817, -73.985428, 'd9e39b5b-b8e5-4f6d-a16d-0d6c23c8a7df');

-- Insert Review data
INSERT INTO Review (id, text, rating, user_id, place_id) 
VALUES ('a2e1f420-02a2-4905-b7d2-3d0d89f64872', 'Great place, highly recommend!', 5, 'd9e39b5b-b8e5-4f6d-a16d-0d6c23c8a7df', 'c55d8d7d-cf02-48ed-a97f-9d8a1c87d5a7');
