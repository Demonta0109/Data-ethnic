-- CTP 4 - setup (run once as shopfast_admin). Creates a clean, typed "analytics" layer from raw.
-- docker exec -i shopfast-db psql -U shopfast_admin -d shopfast < 00_setup_analytics.sql
CREATE SCHEMA IF NOT EXISTS analytics;
DROP TABLE IF EXISTS analytics.customers CASCADE;
CREATE TABLE analytics.customers AS
SELECT DISTINCT
    customer_id::int                                         AS customer_id,
    initcap(trim(first_name))                                AS first_name,
    initcap(trim(last_name))                                 AS last_name,
    lower(trim(email))                                       AS email,
    phone,
    substring(birth_date from '(\d{4})')::int                AS birth_year,
    city,
    postal_code,
    CASE WHEN upper(trim(country)) IN ('FR','FRANCE','FRA') THEN 'FR'
         WHEN upper(trim(country)) IN ('DE','GERMANY','ALLEMAGNE','DEU') THEN 'DE'
         WHEN upper(trim(country)) IN ('ES','SPAIN','ESPAGNE') THEN 'ES'
         WHEN upper(trim(country)) IN ('BE','BELGIUM','BELGIQUE','BEL') THEN 'BE' END AS country_code,
    marketing_consent = 'true'                               AS has_marketing_consent,
    replace(lower(trim(loyalty_tier)), 'platinium', 'platinum') AS loyalty_tier
FROM raw.customers;
ALTER TABLE analytics.customers ADD PRIMARY KEY (customer_id);

DROP TABLE IF EXISTS analytics.orders CASCADE;
CREATE TABLE analytics.orders AS
SELECT DISTINCT ON (order_id::int) order_id::int AS order_id, customer_id::int AS customer_id,
       NULLIF(order_date, '')::date AS order_date, lower(trim(status)) AS status,
       total_amount_eur::numeric(10,2) AS total_amount_eur
FROM raw.orders ORDER BY order_id::int;

-- Login users for the exercise (LOCAL TRAINING PASSWORDS ONLY)
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ana')    THEN CREATE ROLE ana    LOGIN PASSWORD 'training'; END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'mkt')    THEN CREATE ROLE mkt    LOGIN PASSWORD 'training'; END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ds')     THEN CREATE ROLE ds     LOGIN PASSWORD 'training'; END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'sup_fr') THEN CREATE ROLE sup_fr LOGIN PASSWORD 'training'; END IF;
END $$;
SELECT 'analytics.customers' AS t, count(*) FROM analytics.customers UNION ALL SELECT 'analytics.orders', count(*) FROM analytics.orders;
