import arcpy
import os
arcpy.env.overwriteOutput = True
input_shp = arcpy.GetParameterAsText(0)
clip_shp = arcpy.GetParameterAsText(1)
output_directory = arcpy.GetParameterAsText(2)
clipped_output_shp = os.path.join(output_directory, "Inside_Output.shp")
outside_clipped_shp = os.path.join(output_directory, "Outside_Output.shp")
arcpy.Clip_analysis(input_shp, clip_shp, clipped_output_shp)
if not arcpy.Exists(clipped_output_shp):
    arcpy.AddError("Clipped output shapefile was not created.")
    raise Exception("Clipped output shapefile was not created.")
else:
    print("Clipped output shapefile created successfully:", clipped_output_shp)
arcpy.Erase_analysis(input_shp, clip_shp, outside_clipped_shp)
if not arcpy.Exists(outside_clipped_shp):
    arcpy.AddError("Outside clipped output shapefile was not created.")
    raise Exception("Outside clipped output shapefile was not created.")
else:
    print("Outside clipped output shapefile created successfully:", outside_clipped_shp)
if arcpy.Exists(clipped_output_shp):
    print("Adding field to clipped output shapefile...")
    arcpy.AddField_management(clipped_output_shp, "Area_sqm", "DOUBLE")
    print("Field added to clipped output shapefile.")
if arcpy.Exists(outside_clipped_shp):
    print("Adding field to outside clipped output shapefile...")
    arcpy.AddField_management(outside_clipped_shp, "Area_sqm", "DOUBLE")
    print("Field added to outside clipped output shapefile.")
arcpy.CalculateField_management(clipped_output_shp, "Area_sqm", "!shape.area@SQUAREMETERS!", "PYTHON")
arcpy.CalculateField_management(outside_clipped_shp, "Area_sqm", "!shape.area@SQUAREMETERS!", "PYTHON")
total_area_inside = 0
total_area_outside = 0
with arcpy.da.SearchCursor(clipped_output_shp, ["Area_sqm"]) as cursor:
    for row in cursor:
        total_area_inside += row[0]
with arcpy.da.SearchCursor(outside_clipped_shp, ["Area_sqm"]) as cursor:
    for row in cursor:
        total_area_outside += row[0]
print("Total area inside the clipped area:", total_area_inside, "square meters")
print("Total area outside the clipped area:", total_area_outside, "square meters")