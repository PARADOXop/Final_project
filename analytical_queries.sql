Analytical queries
-- 1.How does a player's volume of participation (categorized as Low, Medium, or High) influence their average ranking points, and what is the distribution of the player base across these tiers?
SELECT
    CASE
        WHEN competitions_played <= 10 THEN 'Low (0-10)'
        WHEN competitions_played <= 20 THEN 'Medium (11-20)'
        ELSE 'High (21+)'
    END AS participation_tier,
    ROUND(AVG(points), 2) AS average_points,
    COUNT(*) AS player_count
FROM tennis.ranking
GROUP BY 1
ORDER BY average_points DESC;

-- 2.Which countries produce the highest-performing tennis players on average, and how large is the professional talent pool in those high-achieving nations?
 SELECT
    c.country, 
    ROUND(AVG(r.points), 2) AS average_points,
    COUNT(c.competitor_id) AS player_count
FROM tennis.ranking r
JOIN tennis.competitor c
    ON r.competitor_id = c.competitor_id
GROUP BY c.country
HAVING COUNT(c.competitor_id) >= 5
ORDER BY average_points DESC;

-- 3.Who are the top 20 "Heavy Hitters" currently active in professional tennis, and which tour do they dominate based on their ranking points?
SELECT
    c.name,
    r.points,
    r.competitions_played,
    r.tour
FROM tennis.ranking r
JOIN tennis.competitor c
    ON r.competitor_id = c.competitor_id
WHERE r.points > 500
ORDER BY r.points DESC
LIMIT 20;

--4.Which players demonstrate the highest "Point Efficiency" by maximizing their ranking gains while minimizing the number of tournaments played?
SELECT
    c.name, 
    r.points, 
    r.competitions_played,
    ROUND((r.points * 1.0 / NULLIF(r.competitions_played, 0))::numeric, 2) AS efficiency_ratio
FROM tennis.ranking r
JOIN tennis.competitor c 
    ON r.competitor_id = c.competitor_id
ORDER BY efficiency_ratio DESC
LIMIT 10;


--5.Which tennis complexes serve as the primary infrastructure hubs by housing multiple courts or venues in a single location?
SELECT cx.name AS complex_name, COUNT(v.id) AS court_count
FROM tennis.complex cx
JOIN tennis.venue v ON cx.complex_id = v.complex_id
GROUP BY cx.name
HAVING COUNT(v.id) > 1
ORDER BY court_count DESC;

--6.Which nations produce professional tennis talent despite having no registered physical venues or tournament infrastructure within their borders?
SELECT DISTINCT c.country
FROM tennis.competitor c
LEFT JOIN tennis.venue v ON c.country = v.country_name
WHERE v.id IS NULL
ORDER BY c.country;

--7.How are professional tennis competitions distributed across different organizational categories, and which tiers host the highest volume of events?

SELECT 
    cat.category_name AS category_name, 
    COUNT(comp.id) AS total_events
FROM tennis.competition comp
JOIN tennis.category cat
    ON comp.category_id = cat.id
GROUP BY cat.category_name
ORDER BY total_events DESC;

--8.How does a player's frequency of competition correlate with their ranking success and rank stability?

SELECT
    CASE 
        WHEN competitions_played <= 15 THEN 'Low (<=15)'
        WHEN competitions_played BETWEEN 16 AND 25 THEN 'Moderate (16-25)'
        ELSE 'High (>25)'
    END AS activity_tier,
    ROUND(AVG(points)::numeric, 2) AS average_points,
    ROUND(AVG(ABS(movement))::numeric, 2) AS average_volatility
FROM tennis.ranking
GROUP BY 1
ORDER BY average_points DESC;