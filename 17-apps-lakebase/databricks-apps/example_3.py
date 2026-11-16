# Streamlit app querying a warehouse
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import os
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

cfg = Config()     # app service principal credentials are injected
conn = sql.connect(server_hostname=cfg.host,
                   http_path=f"/sql/1.0/warehouses/{os.environ['WAREHOUSE_ID']}",
                   credentials_provider=lambda: cfg.authenticate)
region = st.selectbox("Region", ["EMEA", "AMER", "APAC"])
with conn.cursor() as cur:
    cur.execute("SELECT order_date, SUM(amount) AS revenue FROM main.gold.fact_orders "
                "WHERE region = :r GROUP BY order_date ORDER BY order_date", {"r": region})
    st.line_chart(cur.fetchall_arrow().to_pandas(), x="order_date", y="revenue")
