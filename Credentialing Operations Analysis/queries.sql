-- Part 2: Data Analysis Queries
-- Database: providers.db
-- Table: provider_registry

--1Provider Count: How many total individual providers are in your database for each of the three states (NY, CA, TX)?

SELECT 
    location_state,
    COUNT(*) as provider_count
FROM provider_registry 
GROUP BY location_state 
ORDER BY provider_count DESC;


--2Top Specialties: What are the Top 10 most common provider specialties (based on taxonomy) across all three states combined?

SELECT 
    primary_specialty AS Top_10_Common_Specialties,
    COUNT(*) as provider_count
FROM provider_registry 
WHERE primary_specialty IS NOT NULL
GROUP BY primary_specialty 
ORDER BY provider_count DESC 
LIMIT 10;



--3 Cardiology in New York: List the NPI, Full Name, and Practice Address City for all providers in New York whose primary specialty is related to 'Cardiology'.

SELECT
      npi,
	  full_name,
	  location_city as practice_address_city
FROM provider_registry
WHERE location_state = 'NY'
AND LOWER(primary_specialty) LIKE '%cardiology%' ;


--4Data Quality Check: Identify providers who may have incomplete data.
-- Write a query to find the count and percentage of providers in your table who are missing a first name and last name

SELECT 
    COUNT(*) as missing_name_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM provider_registry), 2) as missing_name_percentage
FROM provider_registry 
WHERE first_name IS NULL AND last_name IS NULL;




--5. Group Practice Analysis: A common operational challenge is identifying providers who might be part of the same group practice.
-- Write a query to find any address that is shared by 5 or more different individual providers in your dataset



WITH all_addresses AS (

    -- LOCATION addresses
    SELECT
        npi,
        location_address_line1 AS address_line1,
        location_city           AS city,
        location_state          AS state,
        location_postal_code    AS postal_code,
        'LOCATION'              AS address_type
    FROM provider_registry
    WHERE location_address_line1 != 'Unknown'
      AND location_city != 'Unknown'
      AND location_state != 'Unknown'
      AND location_postal_code != 'Unknown'

    UNION ALL

    -- MAILING addresses
    SELECT
        npi,
        mailing_address_line1  AS address_line1,
        mailing_city           AS city,
        mailing_state          AS state,
        mailing_postal_code    AS postal_code,
        'MAILING'              AS address_type
    FROM provider_registry
    WHERE mailing_address_line1 != 'Unknown'
      AND mailing_city != 'Unknown'
      AND mailing_state != 'Unknown'
      AND mailing_postal_code != 'Unknown'
)

SELECT
    address_type,
    address_line1,
    city,
    state,
    postal_code,
    COUNT(DISTINCT npi) AS provider_count
FROM all_addresses
GROUP BY
    address_type,
    address_line1,
    city,
    state,
    postal_code
HAVING COUNT(DISTINCT npi) >= 5
ORDER BY provider_count DESC;