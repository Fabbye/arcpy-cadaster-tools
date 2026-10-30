# 01 e-Terra CGXML to shapefiles

Turns every CGXML file downloaded from e-Terra into shapefiles: one for the land and one for each building on it. This makes the geometry of a whole administrative unit visible in ArcMap in one run.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../docs/images/tool01_cgxml_to_shapefiles-dark.png">
  <img alt="Part of the CGXML file 50103.cgxml next to the two shapefiles made from it: 50103.shp for the land and 50103_C1.shp for its building" src="../../docs/images/tool01_cgxml_to_shapefiles.png">
</picture>

**Files:** `CGXML_IE-SHP.py` (script), `CGXMLIE_SHP.tbx` (toolbox, tool name `CGXMLETERRA-SHP`)

## Parameters

This is the tool in ArcMap:

<img alt="The CGXMLETERRA-SHP tool open in ArcMap, with the folder of CGXML files and the output folder filled in" src="../../docs/images/arcmap_tool01.png" width="640">

| Parameter | What to give it |
|-----------|-----------------|
| Input_CGXML_Folder | Folder with the `.cgxml` files from e-Terra. ArcMap does not show `.cgxml` files in the browse dialog, so the folder can look empty. That is normal. |
| Output_SHP_Folder | Folder for the new shapefiles. Type or paste the path, and create the folder first. |

## Output

* One shapefile per land, named after its e-Terra ID (`E2IDENTIFIER`), with the field `ID`.
* One shapefile per building, named `<land ID>_<construction code>` (for example `50101_C1.shp`), with the fields `ID_IMOBIL` (the land it stands on) and `COD_CTIE` (the construction code).
* All in Stereo 70 (EPSG:31700). Dashes in IDs become underscores in file names.

Land and buildings without coordinates are skipped.

## Try it

Run it on `sample_data/eterra_cgxml`. You get 13 land shapefiles and 17 building shapefiles. Then merge them with [tool 02](../02-merge-land-and-buildings).
