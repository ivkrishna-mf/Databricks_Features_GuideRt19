# Rescue mode with type hints
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/pay/_schema")
    .option("cloudFiles.schemaEvolutionMode", "rescue")
    .option("cloudFiles.schemaHints", "amount DECIMAL(18,2), paid_at TIMESTAMP")
    .load("/Volumes/main/landing/payments/"))
bad = df.where("_rescued_data IS NOT NULL")     # route these to a quarantine table
