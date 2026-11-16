# Prepare tables so Genie understands them
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("COMMENT ON TABLE main.gold.fact_orders IS 'One row per order line. Amount is net of tax in EUR.'")
spark.sql("ALTER TABLE main.gold.fact_orders ALTER COLUMN region COMMENT 'Sales region: EMEA, AMER or APAC'")
spark.sql("ALTER TABLE main.gold.fact_orders ADD CONSTRAINT fk_cust FOREIGN KEY (customer_sk) REFERENCES main.gold.dim_customer")
