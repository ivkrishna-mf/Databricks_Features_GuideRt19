# Install a library on a classic cluster
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute
w = WorkspaceClient()
w.libraries.install(cluster_id="0123-456789-abc", libraries=[
    compute.Library(pypi=compute.PythonPyPiLibrary(package="rapidfuzz==3.9.7")),
    compute.Library(whl="/Volumes/main/ops/libs/orders_lib-1.4.0-py3-none-any.whl")])
for s in w.libraries.cluster_status(cluster_id="0123-456789-abc"):
    print(s.library, s.status)
