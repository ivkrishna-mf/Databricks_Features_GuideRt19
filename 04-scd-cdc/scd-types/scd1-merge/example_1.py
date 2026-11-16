# Batch upsert with deletes
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F, Window
from delta.tables import DeltaTable
w = Window.partitionBy("customer_id").orderBy(F.col("seq").desc())
latest = changes.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")

(DeltaTable.forName(spark, "main.silver.customers").alias("t")
    .merge(latest.alias("s"), "t.customer_id = s.customer_id")
    .whenMatchedDelete(condition="s.op = 'D'")
    .whenMatchedUpdateAll(condition="s.seq > t.seq")
    .whenNotMatchedInsertAll(condition="s.op <> 'D'")
    .execute())
