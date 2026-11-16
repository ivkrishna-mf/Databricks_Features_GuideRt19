# Stream the feed into a downstream MERGE
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from delta.tables import DeltaTable
def apply(batch, _):
    latest = batch.where("_change_type <> 'update_preimage'")   # dedupe per key in real code
    (DeltaTable.forName(batch.sparkSession, "main.gold.customer_360").alias("t")
        .merge(latest.alias("s"), "t.customer_id = s.customer_id")
        .whenMatchedDelete(condition="s._change_type = 'delete'")
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

(spark.readStream.option("readChangeFeed", "true").table("main.silver.customers")
    .writeStream.foreachBatch(apply)
    .option("checkpointLocation", "/Volumes/main/ops/chk/customer_360").start())
