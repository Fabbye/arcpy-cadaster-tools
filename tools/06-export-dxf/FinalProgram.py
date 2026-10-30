import arcpy
import os
import re
input_layer = arcpy.GetParameterAsText(0)
output_folder = arcpy.GetParameterAsText(1)
field_name1 = arcpy.GetParameterAsText(2)
field_name2 = arcpy.GetParameterAsText(3)
def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename[:100]
def get_unique_filename(output_folder, base_name):
    output_dxf = os.path.join(output_folder, "{}.dxf".format(base_name))
    count = 1
    while os.path.exists(output_dxf):
        output_dxf = os.path.join(output_folder, "{}({}).dxf".format(base_name, count))
        count += 1
    return output_dxf
def export_to_dxf(input_layer, output_folder, field_name1, field_name2=None):
    arcpy.env.workspace = os.path.dirname(input_layer)
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            arcpy.AddError("Failed to create output folder: {}".format(e))
            return
    try:
        if field_name2:
            attribute_pairs = set((row[0], row[1]) for row in arcpy.da.SearchCursor(input_layer, [field_name1, field_name2]))
        else:
            attribute_pairs = set((row[0], None) for row in arcpy.da.SearchCursor(input_layer, [field_name1]))
        for attribute_value1, attribute_value2 in attribute_pairs:
            if attribute_value2 is not None:
                base_name = sanitize_filename("{}_{}".format(attribute_value1, attribute_value2))
                where_clause = "{} = '{}' AND {} = '{}'".format(field_name1, attribute_value1, field_name2, attribute_value2)
            else:
                base_name = sanitize_filename("{}".format(attribute_value1))
                where_clause = "{} = '{}'".format(field_name1, attribute_value1)
            arcpy.management.MakeFeatureLayer(input_layer, "temp_layer", where_clause)
            with arcpy.da.SearchCursor("temp_layer", ["SHAPE@"]) as cursor:
                for row in cursor:
                    geometry = row[0]
                    if geometry is None:
                        arcpy.AddMessage("Skipping geometry with null value for attributes {} and {}.".format(attribute_value1, attribute_value2))
                        continue
                    output_dxf = get_unique_filename(output_folder, base_name)
                    temp_feature_class = "in_memory\\temp_feature"
                    if arcpy.Exists(temp_feature_class):
                        arcpy.management.Delete(temp_feature_class)
                    arcpy.management.CopyFeatures([geometry], temp_feature_class)
                    arcpy.ExportCAD_conversion(temp_feature_class, "DXF_R2010", output_dxf, "Ignore_Filenames_in_Tables", "Overwrite_Existing_Files")
                    arcpy.management.Delete(temp_feature_class)
                    arcpy.AddMessage("Exported: {}".format(output_dxf))
            arcpy.management.Delete("temp_layer")
    except Exception as e:
        arcpy.AddError("An error occurred: {}".format(e))
export_to_dxf(input_layer, output_folder, field_name1, field_name2)