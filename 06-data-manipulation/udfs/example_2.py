# Unity Catalog SQL and Python functions
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
spark.sql("""
CREATE OR REPLACE FUNCTION main.fn.fiscal_quarter(d DATE) RETURNS STRING
RETURN concat('FY', year(add_months(d, 6)), '-Q', quarter(add_months(d, 6)))""")

spark.sql("""
CREATE OR REPLACE FUNCTION main.fn.clean_phone(p STRING) RETURNS STRING
LANGUAGE PYTHON AS $$
import re
return re.sub(r'[^0-9+]', '', p) if p else None
$$""")
spark.sql("GRANT EXECUTE ON FUNCTION main.fn.fiscal_quarter TO `analysts`")
