# Storage credentials, external locations and volumes

Available since ~2022 · Part of [Accounts, workspaces and identity](../README.md)

## What it is

A storage credential wraps a cloud identity (IAM role, managed identity, service account). An external location pairs a credential with a storage path and is what you grant on. Volumes govern non-tabular files (CSV drops, images, PDFs, model artifacts) under Unity Catalog with paths like `/Volumes/catalog/schema/volume`.

## How it flows

1. **Cloud identity**: Role or managed identity with access to the bucket.
2. **Storage credential**: Registered in Unity Catalog.
3. **External location**: Credential plus path, with file events optional.
4. **Grants**: READ FILES, WRITE FILES, CREATE EXTERNAL TABLE or VOLUME.
5. **Use**: External tables, external volumes, Auto Loader sources.

```
[Cloud identity] --> [Storage credential] --> [External location] --> [Grants] --> [Use]
```

## When to choose it

**Choose it when**

- Landing zones and any file access.

**Pick something else when**

- Instance profiles, DBFS mounts and keys in Spark configs: legacy patterns that bypass governance.

## Senior engineer verdict

> Mounts are the most common legacy pattern I remove in migrations. Volumes give the same convenient paths with permissions and audit.

## Examples

### 1. External location and grants

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE EXTERNAL LOCATION IF NOT EXISTS landing_zone
URL 's3://acme-landing/'
WITH (STORAGE CREDENTIAL acme_landing_role)
COMMENT 'Raw drops from partners'""")
spark.sql("GRANT READ FILES ON EXTERNAL LOCATION landing_zone TO `data_engineers`")
```

### 2. Managed and external volumes

File: [`example_2.py`](example_2.py)

```python
spark.sql("CREATE VOLUME IF NOT EXISTS main.landing.scratch")                     # managed
spark.sql("CREATE EXTERNAL VOLUME main.landing.partner LOCATION 's3://acme-landing/partner/'")
spark.sql("GRANT READ VOLUME ON VOLUME main.landing.partner TO `analysts`")
pdfs = spark.read.format("binaryFile").load("/Volumes/main/landing/partner/contracts/*.pdf")
```

## Traps and gotchas

- External locations cannot overlap each other or managed storage paths.
- Volumes hold files; you cannot query a volume as a table without reading the files.
