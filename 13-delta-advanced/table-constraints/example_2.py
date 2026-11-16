# Add a CHECK constraint and a foreign key
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("ALTER TABLE main.gold.fact_orders ADD CONSTRAINT positive_amount CHECK (amount >= 0)")
spark.sql("""
ALTER TABLE main.gold.fact_orders ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_sk) REFERENCES main.gold.dim_customer""")
spark.sql("SHOW TBLPROPERTIES main.gold.fact_orders").where("key LIKE 'delta.constraints%'").show(truncate=False)
