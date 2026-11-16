# External location and grants
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE EXTERNAL LOCATION IF NOT EXISTS landing_zone
URL 's3://acme-landing/'
WITH (STORAGE CREDENTIAL acme_landing_role)
COMMENT 'Raw drops from partners'""")
spark.sql("GRANT READ FILES ON EXTERNAL LOCATION landing_zone TO `data_engineers`")
