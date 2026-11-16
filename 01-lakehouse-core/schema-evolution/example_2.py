# MERGE that evolves the target schema
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from delta.tables import DeltaTable
(DeltaTable.forName(spark, "main.silver.customers").alias("t")
    .merge(updates.alias("s"), "t.customer_id = s.customer_id")
    .withSchemaEvolution()
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute())
