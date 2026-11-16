CREATE OR REFRESH STREAMING TABLE dim_customer_history;

CREATE FLOW customer_cdc AS AUTO CDC INTO dim_customer_history
FROM stream(main.bronze.customers_cdc)
KEYS (customer_id)
APPLY AS DELETE WHEN op = 'DELETE'
SEQUENCE BY commit_ts
COLUMNS * EXCEPT (op, commit_ts)
STORED AS SCD TYPE 2;
