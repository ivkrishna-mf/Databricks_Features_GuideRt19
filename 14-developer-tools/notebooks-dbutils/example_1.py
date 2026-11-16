# Widgets as parameters and files with dbutils
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
dbutils.widgets.text("run_date", "2026-11-15", "Run date")
dbutils.widgets.dropdown("env", "dev", ["dev", "prod"])
run_date = dbutils.widgets.get("run_date")

for f in dbutils.fs.ls("/Volumes/main/landing/orders/")[:5]:
    print(f.name, f.size)
dbutils.fs.cp("/Volumes/main/landing/orders/a.json", "/Volumes/main/archive/orders/a.json")
