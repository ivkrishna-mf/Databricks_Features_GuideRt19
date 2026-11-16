# Query in place versus copy
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Federation: query the source directly, nothing copied
emea = spark.table("crm.public.accounts").where("region = 'EMEA'")
# Sharing: provider data mounted as a catalog, nothing copied
shared = spark.table("partner_retail.gold.daily_sales")
# Ingest when you need history, heavy joins or low query latency
emea.write.mode("overwrite").saveAsTable("main.bronze.crm_accounts_snapshot")
