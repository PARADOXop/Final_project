-- 1. CREATE SCHEMA 
CREATE SCHEMA IF NOT EXISTS tennis;



---------------------------------------------------------------------------
-- 2. create table

create table if not exists "tennis".category(
id VARCHAR(50) PRIMARY KEY,
category_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS "tennis".competition (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    category_id VARCHAR(50) NOT NULL
);


CREATE TABLE "tennis".complex (
    complex_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE "tennis".venue (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(7) NOT NULL,
    timezone VARCHAR(100) NOT NULL
);

CREATE TABLE "tennis".competitor (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(50) NOT NULL,
    abbreviation VARCHAR(20) NOT NULL
);

CREATE TABLE "tennis".ranking (
    rank_position INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50) NOT NULL,
    gender VARCHAR(20),
    year INT,
    week INT,
    tour VARCHAR(50),
    id VARCHAR(50) PRIMARY KEY
);

-------------------------------------------
-- 3. validate after data loading
SELECT * FROM tennis.category;
select * from tennis.competition;
select * from tennis.venue;
select * from tennis.complex;
select * from tennis.competitor;
select * from tennis.ranking;



-------------------------------------------------
/*
DROP TABLE IF EXISTS "tennis".ranking CASCADE;
DROP TABLE IF EXISTS "tennis".venue CASCADE;
DROP TABLE IF EXISTS "tennis".competition CASCADE;
DROP TABLE IF EXISTS "tennis".competitor CASCADE;
DROP TABLE IF EXISTS "tennis".complex CASCADE;
DROP TABLE IF EXISTS "tennis".category CASCADE;

*/
------------------------------------------------------
-- 4. SANITY CHECK

SELECT DISTINCT c.category_id
FROM "tennis".competition c
LEFT JOIN "tennis".category cat
    ON c.category_id = cat.id
WHERE cat.id IS NULL;


SELECT DISTINCT r.competitor_id
FROM "tennis".ranking r
LEFT JOIN "tennis".competitor c
    ON r.competitor_id = c.competitor_id
WHERE c.competitor_id IS NULL;


--------------------------------------------------------------
-- 5. Relationship

ALTER TABLE "tennis".competition
ADD CONSTRAINT fk_competition_category
FOREIGN KEY (category_id)
REFERENCES "tennis".category(id);

ALTER TABLE "tennis".venue
ADD CONSTRAINT fk_venue_complex
FOREIGN KEY (complex_id)
REFERENCES "tennis".complex(complex_id);

ALTER TABLE "tennis".ranking
ADD CONSTRAINT fk_ranking_competitor
        FOREIGN KEY (competitor_id)
        REFERENCES "tennis".competitor(competitor_id);

ALTER TABLE "tennis".competitor
DROP CONSTRAINT fk_ranking_competitor;