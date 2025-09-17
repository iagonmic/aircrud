-- HOST
CREATE TABLE Host (
    HostID INT PRIMARY KEY,
    RoomsRent INT
);

-- ROOM TYPE
CREATE TABLE RoomType (
    TypeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) UNIQUE
);

-- LOCATION
CREATE TABLE Location (
    LocalID INT AUTO_INCREMENT PRIMARY KEY,
    Country VARCHAR(100),
    City VARCHAR(100),
    Neighbourhood VARCHAR(100),
    UNIQUE (Country, City, Neighbourhood)
);

-- ROOM
CREATE TABLE Room (
    RoomID INT AUTO_INCREMENT PRIMARY KEY,
    HostID INT,
    TypeID INT,
    LocalID INT,
    Name VARCHAR(500),
    Price DECIMAL(12,2),
    MinimumNights INT,
    Availability INT,
    Coordinates VARCHAR(255),
    FOREIGN KEY (HostID) REFERENCES Host(HostID),
    FOREIGN KEY (TypeID) REFERENCES RoomType(TypeID),
    FOREIGN KEY (LocalID) REFERENCES Location(LocalID)
);

-- REVIEW
CREATE TABLE Review (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    RoomID INT,
    NumberOfReviews INT,
    LastReviewDate DATE,
    ReviewsPerMonth DECIMAL(5,2),
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

-- UPDATE ROOM
CREATE TABLE UpdateRoom (
    UpdateID INT AUTO_INCREMENT PRIMARY KEY,
    RoomID INT,
    UpdateDate DATE,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);