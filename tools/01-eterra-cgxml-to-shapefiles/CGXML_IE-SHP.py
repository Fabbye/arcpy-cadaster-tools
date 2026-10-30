import arcpy
import os
import xml.etree.ElementTree as ET
spatial_ref = arcpy.SpatialReference(31700)
def create_shapefile_with_attributes(points_list, output_name, attributes, spatial_ref, output_folder):
    if not points_list:
        arcpy.AddMessage("No points provided for {}. Skipping...".format(output_name))
        return
    polygon_fc = arcpy.CreateFeatureclass_management("in_memory", "polygon", "POLYGON", spatial_reference=spatial_ref)
    for field_name, field_info in attributes.items():
        arcpy.AddField_management(polygon_fc, field_name, field_info[0], field_length=field_info[1])
    cursor = arcpy.da.InsertCursor(polygon_fc, ['SHAPE@'] + list(attributes.keys()))
    array = arcpy.Array([arcpy.Point(float(x), float(y)) for x, y in points_list])
    polygon = arcpy.Polygon(array, spatial_ref)
    array.removeAll()
    cursor.insertRow([polygon] + [attr[2] for attr in attributes.values()])
    del cursor
    output_shapefile_path = os.path.join(output_folder, output_name)
    arcpy.CopyFeatures_management(polygon_fc, output_shapefile_path)
    arcpy.Delete_management("in_memory")  # Clean up in-memory data
    arcpy.AddMessage("Shapefile created: {}".format(output_shapefile_path))
def process_xml_files(input_folder, output_folder):
    arcpy.env.workspace = input_folder
    arcpy.env.overwriteOutput = True
    cgxml_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.cgxml')]
    arcpy.AddMessage("Found {} CGXML file(s).".format(len(cgxml_files)))
    land_e2_mapping = {}
    for file in cgxml_files:
        file_path = os.path.join(input_folder, file)
        arcpy.AddMessage("Processing file: {}".format(file_path))
        tree = ET.parse(file_path)
        root = tree.getroot()
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None else None
            e2identifier = land.find('E2IDENTIFIER').text if land.find('E2IDENTIFIER') is not None else None
            if land_id and e2identifier:
                land_e2_mapping[land_id] = e2identifier.replace('-', '_')
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None else "Unknown"
            e2identifier = land_e2_mapping.get(land_id, "Unknown")
            points = [(pt.find('X').text, pt.find('Y').text) for pt in root.findall('.//Points[IMMOVABLEID="{}"]'.format(land_id))]
            if points:
                attributes = {'ID': ('TEXT', 50, e2identifier)}
                file_name = "{}.shp".format(e2identifier)
                create_shapefile_with_attributes(points, file_name, attributes, spatial_ref, output_folder)
        for building in root.findall('.//Building'):
            building_id = building.find('BUILDINGID').text if building.find('BUILDINGID') is not None else "Unknown"
            land_id = building.find('LANDID').text if building.find('LANDID') is not None else "Unknown"
            e2identifier = building.find('E2IDENTIFIER').text if building.find('E2IDENTIFIER') is not None else "Unknown"
            cod_ctie = e2identifier.split('-')[1] if '-' in e2identifier else e2identifier
            points = [(pt.find('X').text, pt.find('Y').text) for pt in root.findall('.//Points[BUILDINGID="{}"]'.format(building_id))]
            if points:
                attributes = {
                    'ID_IMOBIL': ('TEXT', 50, land_e2_mapping.get(land_id, "Unknown")),
                    'COD_CTIE': ('TEXT', 50, cod_ctie)
                }
                file_name = "{}_{}.shp".format(land_e2_mapping.get(land_id, "Unknown"), cod_ctie)
                create_shapefile_with_attributes(points, file_name, attributes, spatial_ref, output_folder)
    arcpy.AddMessage("Processing complete. Check output folder for shapefiles.")
if __name__ == '__main__':
    input_folder = arcpy.GetParameterAsText(0)
    output_folder = arcpy.GetParameterAsText(1)
    if not output_folder:
        arcpy.AddError("Output folder is required.")
    else:
        process_xml_files(input_folder, output_folder)
