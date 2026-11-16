# Publish to Kafka through a sink
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

dp.create_sink(name="alerts_kafka", format="kafka",
    options={"kafka.bootstrap.servers": brokers, "topic": "fraud-alerts"})

@dp.append_flow(target="alerts_kafka", name="fraud_to_kafka")
def fraud_to_kafka():
    return (spark.readStream.table("silver_fraud_scores").where("score > 0.9")
        .select(F.col("txn_id").alias("key"), F.to_json(F.struct("*")).alias("value")))
