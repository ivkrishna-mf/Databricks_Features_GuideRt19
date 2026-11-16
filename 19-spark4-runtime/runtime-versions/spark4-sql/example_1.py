# ANSI errors and the try_ functions
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
print(spark.conf.get("spark.sql.ansi.enabled"))     # true on Spark 4 runtimes
df = spark.createDataFrame([("12",), ("abc",)], "v string")
safe = df.select(F.expr("try_cast(v AS INT)").alias("as_int"),
                 F.expr("try_divide(10, 0)").alias("ratio"))
safe.show()      # nulls instead of errors
# df.select(F.col("v").cast("int")).collect()   -> raises CAST_INVALID_INPUT under ANSI
