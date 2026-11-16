# Diagnose a version conflict in a notebook
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
%pip install rapidfuzz==3.9.7 "pydantic>=2.8,<3"
dbutils.library.restartPython()

import importlib.metadata as md
for pkg in ["pydantic", "rapidfuzz", "pyarrow"]:
    print(pkg, md.version(pkg))
