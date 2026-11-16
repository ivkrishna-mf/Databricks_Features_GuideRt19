# Classify incrementally in a pipeline
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.table(name="silver_tickets_classified")
def silver_tickets_classified():
    return (spark.readStream.table("bronze_tickets")
        .withColumn("category",
            F.expr("ai_classify(body, array('billing', 'outage', 'how-to', 'other'))")))
