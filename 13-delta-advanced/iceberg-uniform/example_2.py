# External Spark reading through the Unity Catalog Iceberg REST catalog
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Runs outside Databricks (open-source Spark with the Iceberg runtime jar)
from pyspark.sql import SparkSession
spark = (SparkSession.builder
    .config("spark.sql.catalog.uc", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.uc.type", "rest")
    .config("spark.sql.catalog.uc.uri", "https://<workspace-host>/api/2.1/unity-catalog/iceberg-rest")
    .config("spark.sql.catalog.uc.warehouse", "main")
    .config("spark.sql.catalog.uc.token", "<oauth-token>")
    .getOrCreate())
spark.table("uc.gold.orders_ice").show()
