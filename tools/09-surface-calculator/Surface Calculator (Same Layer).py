import arcpy
import os
arcpy.env.overwriteOutput = True
input_shp = arcpy.GetParameterAsText(0)
clip_shp = arcpy.GetParameterAsText(1)
clipped_output_shp = os.path.join(arcpy.env.scratchFolder, "Temp_Clipped.shp")
outside_output_shp = os.path.join(arcpy.env.scratchFolder, "Temp_Outside.shp")
if not arcpy.ListFields(input_shp, "UID"):
    arcpy.AddField_management(input_shp, "UID", "LONG")
    with arcpy.da.UpdateCursor(input_shp, "UID") as cursor:
        for i, row in enumerate(cursor):
            row[0] = i
            cursor.updateRow(row)
arcpy.Clip_analysis(input_shp, clip_shp, clipped_output_shp)
arcpy.Erase_analysis(input_shp, clip_shp, outside_output_shp)
for shp, area_field in [(clipped_output_shp, "AreaIn"), (outside_output_shp, "AreaOut")]:
    arcpy.AddField_management(shp, area_field, "DOUBLE")
    arcpy.CalculateField_management(shp, area_field, "!shape.area@SQUAREMETERS!", "PYTHON")
arcpy.AddField_management(input_shp, "AreaIn", "DOUBLE")
arcpy.AddField_management(input_shp, "AreaOut", "DOUBLE")
with arcpy.da.UpdateCursor(input_shp, ["UID", "AreaIn", "AreaOut"]) as update_cursor:
    clipped_areas = {row[0]: row[1] for row in arcpy.da.SearchCursor(clipped_output_shp, ["UID", "AreaIn"])}
    outside_areas = {row[0]: row[1] for row in arcpy.da.SearchCursor(outside_output_shp, ["UID", "AreaOut"])}
    for row in update_cursor:
        uid = row[0]
        row[1] = clipped_areas.get(uid, 0)
        row[2] = outside_areas.get(uid, 0)
        update_cursor.updateRow(row)
arcpy.AddField_management(input_shp, "TotalArea", "DOUBLE")
arcpy.CalculateField_management(input_shp, "TotalArea", "!AreaIn! + !AreaOut!", "PYTHON")
arcpy.DeleteField_management(input_shp, "UID")
arcpy.Delete_management(clipped_output_shp)
arcpy.Delete_management(outside_output_shp)
print("Area calculations completed, attribute table updated, UID field removed, and TotalArea field added successfully.")
