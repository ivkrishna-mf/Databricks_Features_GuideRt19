# Managed and external volumes
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("CREATE VOLUME IF NOT EXISTS main.landing.scratch")                     # managed
spark.sql("CREATE EXTERNAL VOLUME main.landing.partner LOCATION 's3://acme-landing/partner/'")
spark.sql("GRANT READ VOLUME ON VOLUME main.landing.partner TO `analysts`")
pdfs = spark.read.format("binaryFile").load("/Volumes/main/landing/partner/contracts/*.pdf")
