# Row filter and column mask on one table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE OR REPLACE FUNCTION main.gov.region_filter(region STRING) RETURNS BOOLEAN
RETURN is_account_group_member('global_admins') OR region = 'EMEA'""")
spark.sql("ALTER TABLE main.gold.sales SET ROW FILTER main.gov.region_filter ON (region)")

spark.sql("""
CREATE OR REPLACE FUNCTION main.gov.mask_email(email STRING) RETURNS STRING
RETURN CASE WHEN is_account_group_member('pii_readers') THEN email
            ELSE concat('***@', split_part(email, '@', 2)) END""")
spark.sql("ALTER TABLE main.gold.customers ALTER COLUMN email SET MASK main.gov.mask_email")
