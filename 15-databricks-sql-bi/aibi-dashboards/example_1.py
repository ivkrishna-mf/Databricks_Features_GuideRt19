# Build the small gold table a dashboard should read
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
(spark.table("main.gold.fact_orders")
    .groupBy("order_date", "region")
    .agg(F.sum("amount").alias("revenue"), F.countDistinct("order_id").alias("orders"))
    .write.mode("overwrite").option("overwriteSchema", "true")
    .saveAsTable("main.gold.dash_daily_region"))
spark.sql("COMMENT ON TABLE main.gold.dash_daily_region IS 'Feeds the Sales overview dashboard'")
