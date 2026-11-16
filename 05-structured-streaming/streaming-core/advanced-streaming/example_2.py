# Real-time mode from Kafka to Kafka
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
scored = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", brokers).option("subscribe", "payments").load()
    .selectExpr("key", "CAST(value AS STRING) AS v")
    .selectExpr("key", "to_json(named_struct('v', v, 'risk', length(v) % 10)) AS value"))

(scored.writeStream.format("kafka")
    .option("kafka.bootstrap.servers", brokers).option("topic", "payments-scored")
    .option("checkpointLocation", "/Volumes/main/ops/chk/payments_rt")
    .outputMode("update")
    .trigger(realTime="5 minutes")      # checkpoint interval; records flow continuously
    .start())
