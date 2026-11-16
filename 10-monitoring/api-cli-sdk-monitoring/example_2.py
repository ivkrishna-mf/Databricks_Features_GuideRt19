# Streaming progress metrics
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from pyspark.sql.streaming import StreamingQueryListener
class Lag(StreamingQueryListener):
    def onQueryStarted(self, e): pass
    def onQueryTerminated(self, e): pass
    def onQueryProgress(self, e):
        p = e.progress
        print(p.name, p.batchId, p.numInputRows, p.inputRowsPerSecond, p.processedRowsPerSecond)
spark.streams.addListener(Lag())
# Ad hoc: query.lastProgress["durationMs"], query.lastProgress["stateOperators"]
