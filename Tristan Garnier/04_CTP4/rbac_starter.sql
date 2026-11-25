-- CTP 4 - Exercise 2 STARTER (run as shopfast_admin after 00_setup_analytics.sql)
-- Goal: each job sees only what it needs. Check with:  python test_access.py

-- 1. Group roles = jobs, not people (done for you)
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'analyst')      THEN CREATE ROLE analyst NOLOGIN; END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'marketing')    THEN CREATE ROLE marketing NOLOGIN; END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'data_science') THEN CREATE ROLE data_science NOLOGIN; END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'support_fr')   THEN CREATE ROLE support_fr NOLOGIN; END IF;
END $$;
GRANT analyst TO ana; GRANT marketing TO mkt; GRANT data_science TO ds; GRANT support_fr TO sup_fr;

-- 2. TODO: make sure nobody but the admin can read schema raw (REVOKE ... FROM PUBLIC)
--          and give USAGE on schema analytics to the 4 group roles

-- 3. TODO: view analytics.v_customers_masked for analysts:
--          customer_id, first initial, email masked like c***@orange.fr (regexp_replace), country_code, loyalty_tier,
--          birth decade instead of birth year. GRANT SELECT to analyst (+ analytics.orders)

-- 4. TODO: view analytics.v_marketing_audience: only customers with has_marketing_consent, only the columns
--          an email campaign needs. GRANT SELECT to marketing

-- 5. TODO: view analytics.v_ds_churn_features: replace customer_id by a SALTED hash
--          encode(sha256(convert_to(customer_id::text || ':your-salt', 'UTF8')), 'hex'), add order features.
--          GRANT SELECT to data_science

-- 6. TODO: support_fr may read customer_id, first_name, last_name, phone, country_code of FRENCH customers only:
--          column-level GRANT + ALTER TABLE ... ENABLE ROW LEVEL SECURITY + CREATE POLICY ... USING (country_code = 'FR')
