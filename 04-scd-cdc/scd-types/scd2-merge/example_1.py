# Close old version and insert new one in a single MERGE
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
from delta.tables import DeltaTable
tgt = DeltaTable.forName(spark, "main.gold.dim_customer")
cur = tgt.toDF().where("is_current")

changed = (src.alias("s").join(cur.alias("t"), "customer_id")
    .where("s.address <> t.address OR s.segment <> t.segment").select("s.*"))

staged = (changed.withColumn("merge_key", F.lit(None).cast("string"))
    .unionByName(src.withColumn("merge_key", F.col("customer_id"))))

(tgt.alias("t").merge(staged.alias("s"), "t.customer_id = s.merge_key AND t.is_current")
    .whenMatchedUpdate(
        condition="t.address <> s.address OR t.segment <> s.segment",
        set={"is_current": "false", "end_date": "s.effective_date"})
    .whenNotMatchedInsert(values={
        "customer_id": "s.customer_id", "address": "s.address", "segment": "s.segment",
        "start_date": "s.effective_date", "end_date": "null", "is_current": "true"})
    .execute())
