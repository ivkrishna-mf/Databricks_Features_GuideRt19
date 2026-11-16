# Parse JSON strings and read XML files
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
raw = spark.createDataFrame([('{"id": 7, "tags": ["a", "b"]}',)], "body string")
schema = F.schema_of_json(F.lit('{"id": 7, "tags": ["a"]}'))
parsed = raw.select(F.from_json("body", schema).alias("j")).select("j.id", F.explode("j.tags").alias("tag"))

books = (spark.read.format("xml").option("rowTag", "book")
    .load("/Volumes/main/landing/catalog/books.xml"))
