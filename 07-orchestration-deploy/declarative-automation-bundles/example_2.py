# Package code the bundle deploys as a wheel
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# src/orders/main.py  (entry point "orders-main" in pyproject.toml, task: python_wheel_task)
import argparse
from pyspark.sql import SparkSession, functions as F

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", default="dev")
    args = p.parse_args()
    spark = SparkSession.builder.getOrCreate()
    (spark.table(f"{args.catalog}.bronze.orders")
        .where("order_id IS NOT NULL")
        .withColumn("loaded_at", F.current_timestamp())
        .write.mode("overwrite").saveAsTable(f"{args.catalog}.silver.orders"))

if __name__ == "__main__":
    main()
