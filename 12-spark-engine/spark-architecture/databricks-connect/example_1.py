# Session against serverless or a profile
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
# or: DatabricksSession.builder.profile("dev").clusterId("0123-456789-abc").getOrCreate()

df = spark.table("samples.nyctaxi.trips").where("trip_distance > 10")
print(df.count())
