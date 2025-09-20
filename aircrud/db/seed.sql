-- HOST
INSERT INTO Host (HostID, RoomsRent)
SELECT `Host ID`, SUM(`Rooms rent by the host`)
FROM air_bnb_listings
GROUP BY `Host ID`;

-- RoomType
INSERT INTO RoomType (Name)
SELECT DISTINCT `Room type`
FROM air_bnb_listings;

-- Location
INSERT INTO Location (Country, City, Neighbourhood)
SELECT DISTINCT Country, City, Neighbourhood
FROM air_bnb_listings;

-- Room
INSERT INTO Room (HostID, TypeID, LocalID, Name, Price, MinimumNights, Availability, Coordinates)
SELECT 
    l.`Host ID`,
    rt.TypeID,
    loc.LocalID,
    l.Name,
    l.`Room Price`,
    l.`Minimum nights`,
    l.Availibility,
    l.Coordinates
FROM air_bnb_listings l
JOIN RoomType rt ON l.`Room type` = rt.Name
JOIN Location loc ON l.Country = loc.Country 
                  AND l.City = loc.City 
                  AND l.Neighbourhood = loc.Neighbourhood;

-- Review
UPDATE air_bnb_listings
SET LastReviewDate = NULL
WHERE LastReviewDate = '';

INSERT INTO Review (RoomID, NumberOfReviews, LastReviewDate, ReviewsPerMonth)
SELECT 
    r.RoomID,
    l.`Number of reviews`,
    l.`Date last review`,
    l.`Number of reviews per month`
FROM air_bnb_listings l
JOIN Room r on r.Coordinates = l.Coordinates;

-- UpdateRoom
UPDATE air_bnb_listings
SET Updated_Date = NULL
WHERE Updated_Date  = '';

INSERT INTO UpdateRoom (RoomID, UpdateDate)
SELECT r.RoomID, l.`Updated Date`
FROM air_bnb_listings l
JOIN Room r on r.Coordinates = l.Coordinates;