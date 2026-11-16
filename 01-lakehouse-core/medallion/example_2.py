# Silver: type, validate, deduplicate
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
silver = (spark.readStream.table("main.bronze.orders")
    .withColumn("order_ts", F.to_timestamp("order_ts"))
    .where("order_id IS NOT NULL")
    .withWatermark("order_ts", "1 hour")
    .dropDuplicatesWithinWatermark(["order_id"]))
(silver.writeStream.option("checkpointLocation", "/Volumes/main/ops/chk/orders_silver")
    .trigger(availableNow=True).toTable("main.silver.orders"))
