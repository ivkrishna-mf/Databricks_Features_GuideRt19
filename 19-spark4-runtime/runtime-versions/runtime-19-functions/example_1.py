# New functions in SQL expressions
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql import functions as F
df = spark.createDataFrame([(3.98765, [1, 2, 3, 4, 5], '{"a": 1, "b": null}')],
                           "x double, arr array<int>, j string")
df.select(F.expr("truncate(x, 2)").alias("truncated"),            # 3.98, no rounding
          F.expr("trim_array(arr, 2)").alias("drop_last_2"),       # [1, 2, 3]
          F.expr("trim_array(arr, -1)").alias("drop_first_1"),     # [2, 3, 4, 5]
          F.expr("variant_strip_nulls(parse_json(j))").alias("clean")).show(truncate=False)
