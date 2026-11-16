# Enable for a catalog and inspect what ran
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER CATALOG main ENABLE PREDICTIVE OPTIMIZATION")
(spark.table("system.storage.predictive_optimization_operations_history")
    .where("catalog_name = 'main'")
    .groupBy("operation_type").count().show())
