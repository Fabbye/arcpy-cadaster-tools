# 07 Generare CG CGXML to shapefiles

Generare CG, the ANCPI program that creates CGXML files, sometimes saves broken geometry. This tool turns the files it made into shapefiles, so the geometry can be checked before anything is uploaded to e-Terra.

It works like [tool 01](../01-eterra-cgxml-to-shapefiles), but reads the structure of Generare CG files, where every property is identified by its temporary CADGEN number.

This is the result on a real project, where 125 Generare CG files became one shapefile per land and per building. The administrative unit code is blurred:

<img alt="ArcMap with one layer for every land and building read from Generare CG files, and the table of building 4544_C1 with its land ID and construction code" src="../../docs/images/real_tool07_result.png">

**Files:** `CGXML_CADGEN-SHP.py` (script), `CGXMLCADGEN_SHP.tbx` (toolbox, tool name `CGXMLCADGEN-SHP`)

## Parameters

This is the tool in ArcMap:

<img alt="The CGXMLCADGEN-SHP tool open in ArcMap, with the CGXML folder and the output folder filled in" src="../../docs/images/arcmap_tool07.png" width="640">

| Parameter | What to give it |
|-----------|-----------------|
| CGXML_Folder | Folder with the CGXML files made by Generare CG. |
| Export_SHP_Folder | Folder for the new shapefiles. Type or paste the path, and create the folder first. |

While it runs, the window lists every file it reads and every shapefile it creates:

<img alt="The tool running: it found 125 CGXML files and lists each file it reads and each shapefile it creates" src="../../docs/images/real_tool07_run.png" width="640">

## Output

* One shapefile per land, named after its CADGEN number, with `SIRSUP`, `ID` and `SECTOR`.
* One shapefile per building, named like `113_C1.shp`, with `SIRSUP`, `ID_IMOBIL` and `COD_CTIE`.

The tool warns about every land or building without geometry. [Tool 02](../02-merge-land-and-buildings) can merge the output into two layers.

## Try it

Run it on `sample_data/generare_cg_cgxml`. You get 13 land shapefiles and 1 building shapefile.
