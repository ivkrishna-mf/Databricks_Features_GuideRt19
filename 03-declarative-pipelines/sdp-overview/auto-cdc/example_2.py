# SCD type 2: history for selected columns
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
dp.create_streaming_table("dim_customer_history")
dp.create_auto_cdc_flow(
    target="dim_customer_history",
    source="customers_cdc",
    keys=["customer_id"],
    sequence_by=col("commit_ts"),
    apply_as_deletes=expr("op = 'DELETE'"),
    except_column_list=["op", "commit_ts"],
    stored_as_scd_type=2,
    track_history_column_list=["address", "segment"])
# Current rows: WHERE __END_AT IS NULL
