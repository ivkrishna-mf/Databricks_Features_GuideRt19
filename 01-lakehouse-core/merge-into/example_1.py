# Upsert with a deduplicated source
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F, Window
from delta.tables import DeltaTable
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc())
latest = updates.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")

(DeltaTable.forName(spark, "main.silver.customers").alias("t")
    .merge(latest.alias("s"), "t.customer_id = s.customer_id")
    .whenMatchedUpdateAll(condition="s.updated_at > t.updated_at")
    .whenNotMatchedInsertAll()
    .execute())
