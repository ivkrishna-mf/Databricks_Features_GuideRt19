# pytest fixture shared by every test
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
# tests/conftest.py
import pytest
from databricks.connect import DatabricksSession

@pytest.fixture(scope="session")
def spark():
    return DatabricksSession.builder.serverless().getOrCreate()
