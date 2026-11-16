# pandas UDF and a plain Python UDF
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import pandas as pd
from pyspark.sql import functions as F

@F.pandas_udf("double")
def net_amount(gross: pd.Series, tax_rate: pd.Series) -> pd.Series:
    return gross / (1 + tax_rate)

@F.udf("string")
def initials(name):
    return "".join(p[0].upper() for p in name.split()) if name else None

df = orders.select("order_id", net_amount("gross", "tax_rate").alias("net"), initials("customer_name"))
