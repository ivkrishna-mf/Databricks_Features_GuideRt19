# Read a Lakebase table into Spark over JDBC
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
token = WorkspaceClient().config.oauth_token().access_token
feedback = (spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://<lakebase-host>:5432/databricks_postgres?sslmode=require")
    .option("dbtable", "app.feedback")
    .option("user", "<your-user-or-service-principal>")
    .option("password", token)
    .load())
feedback.write.mode("overwrite").saveAsTable("main.bronze.app_feedback")
