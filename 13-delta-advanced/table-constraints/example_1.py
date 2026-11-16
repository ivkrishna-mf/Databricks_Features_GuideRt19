# Create a dimension with identity, generated and default columns
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE TABLE main.gold.dim_customer (
  customer_sk  BIGINT GENERATED ALWAYS AS IDENTITY,
  customer_id  STRING NOT NULL,
  signup_ts    TIMESTAMP,
  signup_date  DATE GENERATED ALWAYS AS (CAST(signup_ts AS DATE)),
  status       STRING DEFAULT 'active',
  CONSTRAINT dim_customer_pk PRIMARY KEY (customer_sk)
) TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')""")
