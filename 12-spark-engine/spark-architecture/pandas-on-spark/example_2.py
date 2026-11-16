# One forecast per store with applyInPandas
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import pandas as pd
def fit_store(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.sort_values("day")
    trend = pdf["sales"].rolling(7, min_periods=1).mean().iloc[-1]
    return pd.DataFrame({"store_id": [pdf["store_id"].iloc[0]], "next_day_forecast": [trend]})

forecasts = (spark.table("main.silver.daily_sales")
    .groupBy("store_id")
    .applyInPandas(fit_store, schema="store_id string, next_day_forecast double"))
