# Use an installed listing
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("SHOW SCHEMAS IN acme_weather_data").show()
spark.sql("GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG acme_weather_data TO `analysts`")
spark.sql("""
CREATE OR REPLACE VIEW main.ref.daily_weather AS
SELECT station_id, obs_date, avg_temp_c FROM acme_weather_data.public.daily_obs""")
