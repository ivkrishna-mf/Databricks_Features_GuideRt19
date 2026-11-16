# Latest record per key and change detection
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F, Window
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc())
latest = df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")

w2 = Window.partitionBy("sku").orderBy("price_date")
moves = (prices.withColumn("prev_price", F.lag("price").over(w2))
    .where("prev_price IS NOT NULL AND price <> prev_price"))
