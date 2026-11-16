# Point in polygon with spatial functions
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
stores = spark.sql("""
SELECT 'S1' AS store_id,
       st_geomfromtext('POLYGON((-74.02 40.70, -73.97 40.70, -73.97 40.75, -74.02 40.75, -74.02 40.70))') AS zone""")
pings = spark.createDataFrame([("u1", -74.0, 40.72), ("u2", -73.5, 40.9)], "user_id string, lon double, lat double")
inside = (pings.crossJoin(stores)
    .where("st_contains(zone, st_point(lon, lat))")
    .select("user_id", "store_id"))
inside.show()
