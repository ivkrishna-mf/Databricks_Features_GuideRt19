# Automatic keys, and clustering from the DataFrame API
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.silver.orders CLUSTER BY AUTO")

(df.write.mode("overwrite")
    .clusterBy("order_date", "customer_id")
    .saveAsTable("main.silver.orders_v2"))
