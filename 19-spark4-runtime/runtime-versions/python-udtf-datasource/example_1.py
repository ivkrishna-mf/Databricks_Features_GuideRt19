# Python UDTF that splits text into words
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql.functions import udtf

@udtf(returnType="word string, position int")
class SplitWords:
    def eval(self, text: str):
        for i, w in enumerate((text or "").split()):
            yield w.lower(), i

spark.udtf.register("split_words", SplitWords)
spark.sql("SELECT * FROM split_words('Delta Lake on Databricks')").show()
from pyspark.sql.functions import lit
SplitWords(lit("one two")).show()          # DataFrame API
