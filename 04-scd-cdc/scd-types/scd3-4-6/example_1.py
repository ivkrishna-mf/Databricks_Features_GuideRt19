# Type 3: shift the current value into a previous column
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from delta.tables import DeltaTable
(DeltaTable.forName(spark, "main.gold.dim_store").alias("t")
    .merge(updates.alias("s"), "t.store_id = s.store_id")
    .whenMatchedUpdate(condition="t.region <> s.region",
        set={"previous_region": "t.region", "region": "s.region", "region_changed_on": "s.effective_date"})
    .whenNotMatchedInsert(values={"store_id": "s.store_id", "region": "s.region",
        "previous_region": "null", "region_changed_on": "s.effective_date"})
    .execute())
