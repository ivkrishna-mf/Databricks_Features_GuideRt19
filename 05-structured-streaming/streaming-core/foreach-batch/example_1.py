# Idempotent writes to two tables
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
def write_two(batch_df, batch_id):
    batch_df.persist()
    for table in ["main.silver.orders", "main.audit.orders_log"]:
        (batch_df.write.format("delta").mode("append")
            .option("txnAppId", "orders_" + table).option("txnVersion", batch_id)
            .saveAsTable(table))
    batch_df.unpersist()

(spark.readStream.table("main.bronze.orders").writeStream
    .foreachBatch(write_two)
    .option("checkpointLocation", "/Volumes/main/ops/chk/orders_two").start())
