import arcpy
constructii = arcpy.GetParameterAsText(0)
nr_constructii = arcpy.GetParameterAsText(1)
constructii_cuNr_output = arcpy.GetParameterAsText(2)
imobil = arcpy.GetParameterAsText(3)
id_layer = arcpy.GetParameterAsText(4)
id_imobil_output = arcpy.GetParameterAsText(5)
final_output = arcpy.GetParameterAsText(6)
arcpy.SpatialJoin_analysis(
    constructii, nr_constructii, constructii_cuNr_output,
    "JOIN_ONE_TO_MANY", "KEEP_ALL",
    "",
    "INTERSECT"
)
arcpy.SpatialJoin_analysis(
    imobil, id_layer, id_imobil_output,
    "JOIN_ONE_TO_MANY", "KEEP_ALL",
    "",
    "INTERSECT"
)
arcpy.SpatialJoin_analysis(
    constructii_cuNr_output, id_imobil_output, final_output,
    "JOIN_ONE_TO_MANY", "KEEP_COMMON",
    "",
    "WITHIN"
)
