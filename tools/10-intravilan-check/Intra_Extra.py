import arcpy
import os
import xml.etree.ElementTree as ET
def create_shapefile_with_attributes(points_list, attributes, spatial_ref, output_fc):
    if not points_list:
        arcpy.AddWarning("No points provided. Skipping...")
        return
    for field_name, field_info in attributes.items():
        if field_name not in [f.name for f in arcpy.ListFields(output_fc)]:
            arcpy.AddField_management(output_fc, field_name, field_info[0], field_length=field_info[1])
    cursor = arcpy.da.InsertCursor(output_fc, ['SHAPE@'] + list(attributes.keys()))
    array = arcpy.Array([arcpy.Point(float(x), float(y)) for x, y in points_list])
    polygon = arcpy.Polygon(array, spatial_ref)
    array.removeAll()
    cursor.insertRow([polygon] + [attr[2] for attr in attributes.values()])
    del cursor
def determine_intr_extr_value(parcels):
    return any(parcel.find('INTRAVILAN') is not None and parcel.find('INTRAVILAN').text.lower() == 'true' for parcel in parcels)
def main(input_folder, output_file):
    arcpy.env.workspace = input_folder
    arcpy.env.overwriteOutput = True
    spatial_reference = arcpy.SpatialReference(31700)
    merged_fc = arcpy.CreateFeatureclass_management(
        "in_memory", "merged", "POLYGON", spatial_reference=spatial_reference
    )
    cgxml_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.cgxml')]
    arcpy.AddMessage("Found {} CGXML file(s).".format(len(cgxml_files)))
    for file in cgxml_files:
        file_path = os.path.join(input_folder, file)
        arcpy.AddMessage("Processing file: {}".format(file_path))
        tree = ET.parse(file_path)
        root = tree.getroot()
        sirsups = root.find('.//SIRSUP').text if root.find('.//SIRSUP') is not None else "Unknown"
        parcels = root.findall('.//Parcel')
        intr_extr_value = determine_intr_extr_value(parcels)
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None else "Unknown"
            cadgenno = land.find('CADGENNO').text if land.find('CADGENNO') is not None else "Unknown"
            attributes = {
                'SIRSUP': ('TEXT', 50, sirsups),
                'ID': ('TEXT', 50, cadgenno),
                'SECTOR': ('TEXT', 50, land.find('CADSECTOR').text if land.find('CADSECTOR') is not None else "Unknown"),
                'IntrExtr': ('TEXT', 5, 'True' if intr_extr_value else 'False')
            }
            points = [(pt.find('X').text, pt.find('Y').text) for pt in root.findall('.//Points[IMMOVABLEID="{}"]'.format(land_id))]
            if points:
                create_shapefile_with_attributes(points, attributes, spatial_reference, merged_fc)
            else:
                arcpy.AddWarning("No valid points extracted for land with CADGENNO: {}".format(cadgenno))
    arcpy.CopyFeatures_management(merged_fc, output_file)
    arcpy.AddMessage("Merged shapefile created: {}".format(output_file))
if __name__ == '__main__':
    input_folder = arcpy.GetParameterAsText(0)
    output_file = arcpy.GetParameterAsText(1)
    main(input_folder, output_file)
