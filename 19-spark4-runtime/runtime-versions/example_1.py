# Check the runtime and Spark version from code
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import os
print(spark.version)                                               # Apache Spark version
print(os.environ.get("DATABRICKS_RUNTIME_VERSION"))                # e.g. "19.0"
print(spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion", "serverless"))
