# Connect from a Databricks App with OAuth
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import os
import psycopg
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
token = w.config.oauth_token().access_token        # short-lived, used as the password
with psycopg.connect(host=os.environ["PGHOST"], dbname=os.environ.get("PGDATABASE", "databricks_postgres"),
                     user=os.environ["PGUSER"], password=token, sslmode="require") as conn:
    cur = conn.execute("SELECT segment, lifetime_value FROM serving.customer_profile WHERE customer_id = %s",
                       ("C-1042",))
    print(cur.fetchone())
    conn.execute("INSERT INTO app.feedback (customer_id, note) VALUES (%s, %s)", ("C-1042", "called back"))
