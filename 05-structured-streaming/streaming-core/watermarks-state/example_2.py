# Streaming deduplication with bounded state
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.conf.set("spark.sql.streaming.stateStore.providerClass",
    "com.databricks.sql.streaming.state.RocksDBStateStoreProvider")
dedup = (spark.readStream.table("main.bronze.payments")
    .withWatermark("paid_at", "1 hour")
    .dropDuplicatesWithinWatermark(["payment_id"]))
