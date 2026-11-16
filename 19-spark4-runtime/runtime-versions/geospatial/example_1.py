# Index points into H3 cells and aggregate
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
trips = spark.table("samples.nyctaxi.trips").limit(100000)
cells = (trips.withColumn("cell", F.expr("h3_longlatash3(pickup_longitude, pickup_latitude, 8)"))
    .groupBy("cell").count().orderBy(F.desc("count")))
cells.show(5)
