# Running count per user with transformWithStateInPandas
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
import pandas as pd
from pyspark.sql.streaming import StatefulProcessor, StatefulProcessorHandle
from pyspark.sql.types import StructType, StructField, LongType

class EventCounter(StatefulProcessor):
    def init(self, handle: StatefulProcessorHandle) -> None:
        self.count = handle.getValueState("count", StructType([StructField("n", LongType())]))

    def handleInputRows(self, key, rows, timerValues):
        n = self.count.get()[0] if self.count.exists() else 0
        for pdf in rows:
            n += len(pdf)
        self.count.update((n,))
        yield pd.DataFrame({"user_id": [key[0]], "events": [n]})

    def close(self) -> None:
        pass

counts = (spark.readStream.table("main.silver.events").groupBy("user_id")
    .transformWithStateInPandas(statefulProcessor=EventCounter(),
        outputStructType="user_id string, events long", outputMode="Update", timeMode="None"))
