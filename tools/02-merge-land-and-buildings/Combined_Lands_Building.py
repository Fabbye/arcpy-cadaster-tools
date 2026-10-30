import arcpy
import os
def merge_shapefiles(input_folder, output_path, land_pattern="*.shp", building_pattern="*_*"):
    arcpy.env.workspace = input_folder
    land_shapefiles = [os.path.join(input_folder, f) for f in arcpy.ListFeatureClasses(land_pattern) if "_" not in f]
    building_shapefiles = [os.path.join(input_folder, f) for f in arcpy.ListFeatureClasses(building_pattern)]
    if land_shapefiles:
        arcpy.Merge_management(land_shapefiles, os.path.join(output_path, "Land.shp"))
        arcpy.AddMessage("Merged land shapefiles created at: {}".format(os.path.join(output_path, "Land.shp")))
    else:
        arcpy.AddMessage("No land shapefiles found to merge.")
    if building_shapefiles:
        arcpy.Merge_management(building_shapefiles, os.path.join(output_path, "Buildings.shp"))
        arcpy.AddMessage("Merged building shapefiles created at: {}".format(os.path.join(output_path, "Buildings.shp")))
    else:
        arcpy.AddMessage("No building shapefiles found to merge.")
if __name__ == '__main__':
    input_folder = arcpy.GetParameterAsText(0)
    output_path = arcpy.GetParameterAsText(1)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        arcpy.AddMessage("Output directory created: " + output_path)
    merge_shapefiles(input_folder, output_path)
