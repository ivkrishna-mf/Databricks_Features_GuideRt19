# Geospatial: H3 and spatial types

Available since ~2022 · Part of [Databricks Runtime versions from the beginning to 19](../README.md)

## What it is

Databricks has built-in H3 functions that index latitude and longitude into hexagonal cells for fast spatial joins and aggregation, and native GEOMETRY and GEOGRAPHY types with ST_ functions for points, polygons, distance and containment.

## How it flows

1. **Coordinates**: Longitude and latitude columns.
2. **Index**: h3_longlatash3 at a chosen resolution.
3. **Join on cell**: Equi-join instead of an expensive spatial predicate.
4. **Refine**: ST_ functions for exact containment or distance.
5. **Aggregate**: Counts per cell for maps.

```
[Coordinates] --> [Index] --> [Join on cell] --> [Refine] --> [Aggregate]
```

## When to choose it

**Choose it when**

- Joining points to areas or to each other at scale.
- Heatmaps and proximity analytics.

**Pick something else when**

- Exact geometry checks on billions of pairs without an H3 pre-filter.

## Senior engineer verdict

> Index with H3 first, refine with ST functions second. Turning a spatial join into an equi-join on cell ids is what makes it scale.

## Examples

### 1. Index points into H3 cells and aggregate

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
trips = spark.table("samples.nyctaxi.trips").limit(100000)
cells = (trips.withColumn("cell", F.expr("h3_longlatash3(pickup_longitude, pickup_latitude, 8)"))
    .groupBy("cell").count().orderBy(F.desc("count")))
cells.show(5)
```

### 2. Point in polygon with spatial functions

File: [`example_2.py`](example_2.py)

```python
stores = spark.sql("""
SELECT 'S1' AS store_id,
       st_geomfromtext('POLYGON((-74.02 40.70, -73.97 40.70, -73.97 40.75, -74.02 40.75, -74.02 40.70))') AS zone""")
pings = spark.createDataFrame([("u1", -74.0, 40.72), ("u2", -73.5, 40.9)], "user_id string, lon double, lat double")
inside = (pings.crossJoin(stores)
    .where("st_contains(zone, st_point(lon, lat))")
    .select("user_id", "store_id"))
inside.show()
```

## Traps and gotchas

- H3 resolution trades precision for cell count: higher resolution means smaller cells and more of them.
- Longitude comes before latitude in h3_longlatash3 and st_point.
