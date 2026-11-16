# Idempotent append that survives a retry
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# Same (txnAppId, txnVersion) is written once, even if the task reruns
(df.write.format("delta").mode("append")
    .option("txnAppId", "orders_loader")
    .option("txnVersion", run_number)       # monotonically increasing per app
    .saveAsTable("main.sales.orders"))
