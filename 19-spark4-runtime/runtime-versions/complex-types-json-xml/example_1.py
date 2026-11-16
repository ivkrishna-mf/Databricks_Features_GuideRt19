# Higher-order functions on arrays
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
orders = spark.createDataFrame([(1, [10.0, 25.5, 4.0])], "id int, prices array<double>")
out = orders.select("id",
    F.transform("prices", lambda p: p * 1.2).alias("with_tax"),
    F.filter("prices", lambda p: p > 5).alias("over_5"),
    F.aggregate("prices", F.lit(0.0), lambda acc, p: acc + p).alias("total"),
    F.exists("prices", lambda p: p > 20).alias("has_big_item"))
out.show(truncate=False)
