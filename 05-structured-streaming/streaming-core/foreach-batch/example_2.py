# Streaming aggregation upserted with MERGE (update mode)
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from delta.tables import DeltaTable
def upsert_counts(batch_df, batch_id):
    (DeltaTable.forName(batch_df.sparkSession, "main.gold.user_counts").alias("t")
        .merge(batch_df.alias("s"), "t.user_id = s.user_id")
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

(spark.readStream.table("main.silver.events").groupBy("user_id").count()
    .writeStream.outputMode("update").foreachBatch(upsert_counts)
    .option("checkpointLocation", "/Volumes/main/ops/chk/user_counts").start())
