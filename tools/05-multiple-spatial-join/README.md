# 05 Multiple spatial join

New measurements are usually drawn in AutoCAD or a similar program. A drawing keeps the shapes, but the land IDs and construction codes are only text labels placed inside them. This tool turns the labels into attributes with three spatial joins, so every building knows its construction code and the ID of the land it stands on. That is what Generare CG needs.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../docs/images/tool05_spatial_join-dark.png">
  <img alt="On the left, the drawing with land and building outlines and text labels. On the right, every building linked to its code and to the ID of the land it stands on" src="../../docs/images/tool05_spatial_join.png">
</picture>

**Files:** `FullJoin.py` (script), `SoftwareMultipleJoin.tbx` (toolbox, tool name `MultipleSpatialJoin`)

## Parameters

This is the tool in ArcMap:

<img alt="The MultipleSpatialJoin tool open in ArcMap, with the building, label and land layers and the three outputs filled in" src="../../docs/images/arcmap_tool05.png" width="640">

| Parameter | What to give it |
|-----------|-----------------|
| Constructii | Building polygons. |
| Numar Constructii | Points with the construction codes (C1, C2...). |
| Nr_Constructii_Output | Output: buildings with their codes. |
| Imobil | Land polygons. |
| ID Imobil | Points with the land IDs. |
| ID_Imobil_Output | Output: land with its IDs. |
| Layer Final | Output: buildings with their code and the ID of their land. |

## What it does

1. Buildings get the code of the label point inside them (intersect).
2. Land gets the ID of the label point inside it (intersect).
3. Every building gets the land it lies within, so the final layer holds the building, its code and its land ID.

The first two joins keep every shape, even one without a label. The last join keeps only the buildings that lie within a land parcel. A shape with two labels inside it appears twice in the result, which makes that kind of drawing mistake easy to spot.

## Try it

Use the files in `sample_data/shapefiles`: `Constructii.shp`, `Nr_Constructii.shp`, `Imobile.shp` and `ID_Imobile.shp`. The labels are in the `Text` field, the same way they come out of a CAD export.
