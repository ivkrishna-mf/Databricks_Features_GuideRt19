# Run SQL from any app with the Statement Execution API
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
resp = w.statement_execution.execute_statement(
    warehouse_id=wh.id,
    statement="SELECT region, SUM(amount) AS revenue FROM main.gold.fact_orders WHERE order_date >= :d GROUP BY region",
    parameters=[{"name": "d", "value": "2026-11-01", "type": "DATE"}],
    wait_timeout="30s")
print(resp.status.state, resp.result.data_array[:5])
