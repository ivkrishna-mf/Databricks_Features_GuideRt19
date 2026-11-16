# The same upsert from a stream
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
def upsert(batch_df, batch_id):
    w = Window.partitionBy("customer_id").orderBy(F.col("seq").desc())
    latest = batch_df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")
    (DeltaTable.forName(batch_df.sparkSession, "main.silver.customers").alias("t")
        .merge(latest.alias("s"), "t.customer_id = s.customer_id")
        .whenMatchedUpdateAll(condition="s.seq > t.seq")
        .whenNotMatchedInsertAll().execute())

(spark.readStream.table("main.bronze.customers_cdc").writeStream
    .foreachBatch(upsert)
    .option("checkpointLocation", "/Volumes/main/ops/chk/customers_scd1")
    .trigger(availableNow=True).start())
