# ABAC: one policy for every column tagged as email
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.gold.customers ALTER COLUMN email SET TAGS ('pii' = 'email')")
spark.sql("""
CREATE OR REPLACE FUNCTION main.gov.redact(v STRING) RETURNS STRING RETURN '[redacted]'""")
spark.sql("""
CREATE POLICY mask_pii_email ON CATALOG main
COMMENT 'Mask email columns for everyone except pii_readers'
COLUMN MASK main.gov.redact
TO `account users` EXCEPT `pii_readers`
FOR TABLES
MATCH COLUMNS hasTagValue('pii', 'email') AS c
ON COLUMN c""")
