# Stream-stream join with watermarks and a time bound
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
imp = spark.readStream.table("main.silver.impressions").withWatermark("imp_ts", "2 hours").alias("imp")
clk = spark.readStream.table("main.silver.clicks").withWatermark("clk_ts", "3 hours").alias("clk")
joined = imp.join(clk, F.expr("""
    imp.ad_id = clk.ad_id AND
    clk_ts BETWEEN imp_ts AND imp_ts + INTERVAL 1 HOUR"""), "leftOuter")
