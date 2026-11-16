# Salted hash and generalization in a streaming silver table
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
salt = dbutils.secrets.get("privacy", "email_salt")
silver = (spark.readStream.table("main.bronze.signups")
    .withColumn("email_key", F.sha2(F.concat(F.lit(salt), F.lower("email")), 256))
    .withColumn("age_band", F.concat((F.floor(F.col("age") / 10) * 10).cast("string"), F.lit("s")))
    .withColumn("zip3", F.substring("zip", 1, 3))
    .drop("email", "age", "zip", "full_name"))
