# Whole record as VARIANT
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("singleVariantColumn", "payload")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/events/_schema")
    .load("/Volumes/main/landing/events/"))
typed = df.selectExpr("payload:user.id::string AS user_id", "payload:ts::timestamp AS ts")
