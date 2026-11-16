# Connection and foreign catalog
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE CONNECTION pg_crm TYPE postgresql
OPTIONS (host 'crm.acme.internal', port '5432',
         user secret('crm', 'user'), password secret('crm', 'pwd'))""")
spark.sql("CREATE FOREIGN CATALOG crm USING CONNECTION pg_crm OPTIONS (database 'crm')")
spark.sql("GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG crm TO `analysts`")
