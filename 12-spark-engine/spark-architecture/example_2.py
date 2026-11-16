# repartition, coalesce and AQE
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.conf.set("spark.sql.adaptive.enabled", "true")                 # default on Databricks
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

wide = df.repartition(200, "customer_id")   # full shuffle, even distribution by key
narrow = df.coalesce(8)                     # merges partitions, no shuffle, can be uneven
print(df.rdd.getNumPartitions(), wide.rdd.getNumPartitions(), narrow.rdd.getNumPartitions())
