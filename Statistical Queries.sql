Statistical Queries
---------------------------------------------------------------------------------------

--1.Which countries have the highest number of professional tennis players represented in the database?
SELECT country, COUNT(competitor_id) AS total_players
FROM tennis.competitor
GROUP BY country
ORDER BY total_players DESC
LIMIT 10;
---------------------------------------------------------------------------------------

--2.Which countries possess the most physical tennis venues (courts and stadiums) for professional play?
SELECT country_name, COUNT(id) AS venue_count
FROM tennis.venue
GROUP BY country_name
ORDER BY venue_count DESC;
---------------------------------------------------------------------------------------

--3.What is the distribution of tournament formats (Singles vs. Doubles) across different genders?
SELECT type, gender,  COUNT(id) AS event_count
FROM tennis.competition
GROUP BY type, gender
ORDER BY event_count DESC;
---------------------------------------------------------------------------------------

--4.What are the average ranking points and tournament participation levels for players on different tours (e.g., ATP vs. WTA)?
SELECT tour,
       AVG(points) AS avg_points, 
       AVG(competitions_played) AS avg_participation
FROM tennis.ranking
GROUP BY tour;
---------------------------------------------------------------------------------------

--5.How much did the world rankings fluctuate this week in terms of the average movement, highest climb, and deepest drop?
SELECT AVG(ABS(movement)) AS avg_absolute_movement, 
       MAX(movement) AS highest_climb, 
       MIN(movement) AS deepest_drop
FROM tennis.ranking;
---------------------------------------------------------------------------------------

--6.What is the statistical spread and standard deviation of ranking movements among all ranked players?
SELECT 
    AVG(ABS(movement)) AS average_absolute_shift,
    MIN(movement) AS biggest_rank_drop,
    MAX(movement) AS biggest_rank_climb,
    STDDEV(movement) AS movement_standard_deviation
FROM tennis.ranking;
---------------------------------------------------------------------------------------

--7.Which 10 countries have the highest number of players who currently hold an active professional ranking?
SELECT
    c.country, 
    COUNT(r.id) AS ranked_player_count
FROM tennis.ranking r
JOIN tennis.competitor c
ON r.competitor_id = c.competitor_id
GROUP BY c.country
ORDER BY ranked_player_count DESC
LIMIT 10;
---------------------------------------------------------------------------------------

--8.Which tournament categories (e.g., Grand Slams, Challengers, 250s) host the highest volume of individualcompetitions?
SELECT
    cat.category_name AS category_name, 
    COUNT(comp.id) AS competition_count
FROM tennis.competition comp
JOIN tennis.category cat 
ON comp.category_id = cat.id
GROUP BY cat.category_name
ORDER BY competition_count DESC;
---------------------------------------------------------------------------------------

--Q1. How many categories exist in the dataset?

SELECT COUNT(*) AS total_categories
FROM tennis.category;

---------------------------------------------------------------------------------------
--Q2. How many competitions are recorded?

SELECT COUNT(*) AS total_competitions
FROM tennis.competition;
------------------------------------------------------------------------------------------
--Q3. How many sports complexes exist?

SELECT COUNT(*) AS total_complexes
FROM tennis.complex;
------------------------------------------------------------------------------------------
--Q4. How many venues exist?

SELECT COUNT(*) AS total_venues
FROM tennis.venue;
--------------------------------------------------------------------------------------
--Q5. How many competitors exist?

SELECT COUNT(*) AS total_competitors
FROM tennis.competitor;
---------------------------------------------------------------------------------------
--Q6. What is the highest ranking points achieved by any player?

SELECT MAX(points) AS highest_points
FROM tennis.ranking;
--------------------------------------------------------------------------------------
--Q7. What is the lowest ranking points recorded?

SELECT MIN(points) AS lowest_points
FROM tennis.ranking;

----------------------------------------------------------------------------------------
--Q8. How does ranking movement vary across players?

SELECT competitor_id, AVG(movement) AS avg_movement
FROM tennis.ranking
GROUP BY competitor_id
ORDER BY avg_movement DESC;

------------------------------------------------------------------------------------------
--Q9. Do players who play more competitions have higher ranking points?

SELECT competitions_played, AVG(points) AS avg_points
FROM tennis.ranking
GROUP BY competitions_played
ORDER BY competitions_played;
--------------------------------------------------------------------------------------
--Q10. Which countries produce players with the highest average ranking points?

SELECT c.country, AVG(r.points) AS avg_points
FROM tennis.competitor c
JOIN tennis.ranking r
ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY avg_points DESC;
---------------------------------------------------------------------------
--Q11. Which countries have the most ranked competitors?

SELECT c.country, COUNT(r.competitor_id) AS ranked_players
FROM tennis.competitor c
JOIN tennis.ranking r
ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY ranked_players DESC;
--------------------------------------------------------------------------------------
--Q12. Which timezones host the most tennis venues?

SELECT timezone, COUNT(*) AS venue_count
FROM tennis.venue
GROUP BY timezone
ORDER BY venue_count DESC;
--Q1. How many categories exist in the dataset?

SELECT COUNT(*) AS total_categories
FROM tennis.category;

---------------------------------------------------------------------------------------
--Q2. How many competitions are recorded?

SELECT COUNT(*) AS total_competitions
FROM tennis.competition;
------------------------------------------------------------------------------------------
--Q3. How many sports complexes exist?

SELECT COUNT(*) AS total_complexes
FROM tennis.complex;
------------------------------------------------------------------------------------------
--Q4. How many venues exist?

SELECT COUNT(*) AS total_venues
FROM tennis.venue;
--------------------------------------------------------------------------------------
--Q5. How many competitors exist?

SELECT COUNT(*) AS total_competitors
FROM tennis.competitor;
---------------------------------------------------------------------------------------
--Q6. What is the highest ranking points achieved by any player?

SELECT MAX(points) AS highest_points
FROM tennis.ranking;
--------------------------------------------------------------------------------------
--Q7. What is the lowest ranking points recorded?

SELECT MIN(points) AS lowest_points
FROM tennis.ranking;

----------------------------------------------------------------------------------------
--Q8. How does ranking movement vary across players?

SELECT competitor_id, AVG(movement) AS avg_movement
FROM tennis.ranking
GROUP BY competitor_id
ORDER BY avg_movement DESC;

------------------------------------------------------------------------------------------
--Q9. Do players who play more competitions have higher ranking points?

SELECT competitions_played, AVG(points) AS avg_points
FROM tennis.ranking
GROUP BY competitions_played
ORDER BY competitions_played;
--------------------------------------------------------------------------------------
--Q10. Which countries produce players with the highest average ranking points?

SELECT c.country, AVG(r.points) AS avg_points
FROM tennis.competitor c
JOIN tennis.ranking r
ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY avg_points DESC;
---------------------------------------------------------------------------
--Q11. Which countries have the most ranked competitors?

SELECT c.country, COUNT(r.competitor_id) AS ranked_players
FROM tennis.competitor c
JOIN tennis.ranking r
ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY ranked_players DESC;
--------------------------------------------------------------------------------------
--Q12. Which timezones host the most tennis venues?

SELECT timezone, COUNT(*) AS venue_count
FROM tennis.venue
GROUP BY timezone
ORDER BY venue_count DESC;