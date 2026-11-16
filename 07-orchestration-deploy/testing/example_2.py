# pytest unit test
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.testing import assertDataFrameEqual, assertSchemaEqual
from orders.transforms import with_net, only_paid

def test_net_for_paid_orders(spark):
    src = spark.createDataFrame([(1, "PAID", 120.0), (2, "OPEN", 60.0)], "id int, status string, gross double")
    out = src.transform(only_paid).transform(with_net, 0.2)
    expected = spark.createDataFrame([(1, "PAID", 120.0, 100.0)], "id int, status string, gross double, net double")
    assertSchemaEqual(out.schema, expected.schema)
    assertDataFrameEqual(out, expected)          # ignores row order by default
