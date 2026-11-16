# Custom batch data source
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql.datasource import DataSource, DataSourceReader, InputPartition

class RangeReader(DataSourceReader):
    def __init__(self, options):
        self.n = int(options.get("rows", "10"))
    def partitions(self):
        return [InputPartition(i) for i in range(4)]
    def read(self, partition):
        for i in range(partition.value, self.n, 4):
            yield (i, i * i)

class SquaresSource(DataSource):
    @classmethod
    def name(cls):
        return "squares"
    def schema(self):
        return "n int, sq int"
    def reader(self, schema):
        return RangeReader(self.options)

spark.dataSource.register(SquaresSource)
spark.read.format("squares").option("rows", "20").load().show()
