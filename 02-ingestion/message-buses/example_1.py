# Kafka to bronze
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
raw = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", brokers)
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")
    .option("maxOffsetsPerTrigger", 200000)
    .load())
(raw.selectExpr("CAST(key AS STRING) k", "CAST(value AS STRING) v",
                "topic", "partition", "offset", "timestamp")
    .writeStream.option("checkpointLocation", "/Volumes/main/ops/chk/kafka_orders")
    .toTable("main.bronze.orders_events"))
