# Comments and tags
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("COMMENT ON TABLE main.gold.daily_revenue IS 'Net revenue per day and store, refreshed hourly'")
spark.sql("ALTER TABLE main.gold.daily_revenue ALTER COLUMN revenue COMMENT 'Net of tax, in EUR'")
spark.sql("ALTER TABLE main.gold.daily_revenue SET TAGS ('domain' = 'finance', 'tier' = 'gold')")
spark.sql("SELECT * FROM main.information_schema.table_tags WHERE tag_name = 'domain'").show()
