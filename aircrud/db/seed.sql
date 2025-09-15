-- HOST
INSERT INTO Host (HostID, RoomsRent)
SELECT `Host ID`, AVG(`Rooms rent by the host`)
FROM air_bnb_listings
GROUP BY `Host ID`;

# Conferir com ALEX se vai usar AVG, MAX ou outra coisa e continuar populando a partir de Room (incluso), após rodar Host

-- RoomType
INSERT INTO RoomType (Name)
SELECT DISTINCT `Room type`
FROM air_bnb_listings;

-- Location
INSERT INTO Location (Country, City, Neighbourhood)
SELECT DISTINCT Country, City, Neighbourhood
FROM air_bnb_listings;

-- Room
INSERT INTO Room (RoomID, HostID, TypeID, LocalID, Name, Price, MinimumNights, Availability, Coordinates)
SELECT 
    l.`Room ID`,
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
INSERT INTO Review (RoomID, NumberOfReviews, LastReviewDate, ReviewsPerMonth)
SELECT 
    `Room ID`,
    `Number of reviews`,
    `Date last review`,
    `Number of reviews per month`
FROM air_bnb_listings;

-- UpdateRoom
INSERT INTO UpdateRoom (RoomID, UpdateDate)
SELECT `Room ID`, `Updated Date`
FROM air_bnb_listings;


select abl.`Host ID`, abl.`Rooms rent by the host` from air_bnb_listings abl 
where abl.`Host ID` = '10003042'