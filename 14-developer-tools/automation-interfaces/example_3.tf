resource "databricks_catalog" "sales" {
  name    = "sales"
  comment = "Sales domain"
}

resource "databricks_schema" "gold" {
  catalog_name = databricks_catalog.sales.name
  name         = "gold"
}

resource "databricks_grants" "gold" {
  schema = "${databricks_catalog.sales.name}.${databricks_schema.gold.name}"
  grant {
    principal  = "analysts"
    privileges = ["USE_SCHEMA", "SELECT"]
  }
}
