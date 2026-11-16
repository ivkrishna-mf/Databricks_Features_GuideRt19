# Path syntax and exploding an array
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
SELECT payload:order_id::string AS order_id,
       item.value:sku::string   AS sku,
       item.value:qty::int      AS qty
FROM main.bronze.orders_v,
     LATERAL variant_explode(payload:items) AS item""").show()
