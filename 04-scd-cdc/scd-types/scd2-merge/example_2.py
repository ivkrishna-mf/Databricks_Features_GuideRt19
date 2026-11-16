# Change detection with a hash of tracked columns
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
tracked = ["address", "segment", "tier"]
src_h = src.withColumn("row_hash", F.sha2(F.concat_ws("||", *[F.coalesce(F.col(c).cast("string"), F.lit("")) for c in tracked]), 256))
changed = (src_h.alias("s").join(cur.alias("t"), "customer_id", "left")
    .where("t.customer_id IS NULL OR s.row_hash <> t.row_hash")
    .select("s.*"))
