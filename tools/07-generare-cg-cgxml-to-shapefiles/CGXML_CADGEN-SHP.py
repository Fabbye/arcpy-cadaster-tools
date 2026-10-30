import arcpy
import os
import xml.etree.ElementTree as ET
def create_shapefile_with_attributes(points_list, output_name, attributes, spatial_ref, output_folder):
    if not points_list:
        arcpy.AddWarning("No points provided for {}. Skipping...".format(output_name))
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
    arcpy.Delete_management("in_memory")
    arcpy.AddMessage("Shapefile created: {}".format(output_shapefile_path))
def main(input_folder, output_folder):
    arcpy.env.workspace = input_folder
    arcpy.env.overwriteOutput = True
    land_cadgenno_mapping = {}
    cgxml_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.cgxml')]
    arcpy.AddMessage("Found {} CGXML file(s).".format(len(cgxml_files)))
    for file in cgxml_files:
        file_path = os.path.join(input_folder, file)
        arcpy.AddMessage("Processing file: {}".format(file_path))
        tree = ET.parse(file_path)
        root = tree.getroot()
        spatial_reference = arcpy.SpatialReference(31700)
        sirsups = root.find('.//SIRSUP').text if root.find('.//SIRSUP') is not None else "Unknown"
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None else None
            cadgenno = land.find('CADGENNO').text if land.find('CADGENNO') is not None else None
            if land_id and cadgenno:
                land_cadgenno_mapping[land_id] = cadgenno.replace('-', '_')
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None else "Unknown"
            cadgenno = land_cadgenno_mapping.get(land_id, "Unknown")
            attributes = {
                'SIRSUP': ('TEXT', 50, sirsups),
                'ID': ('TEXT', 50, cadgenno),
                'SECTOR': ('TEXT', 50, land.find('CADSECTOR').text if land.find('CADSECTOR') is not None else "Unknown")
            }
            points = [(pt.find('X').text, pt.find('Y').text) for pt in root.findall('.//Points[IMMOVABLEID="{}"]'.format(land_id))]
            if points:
                file_name = "{}.shp".format(cadgenno)
                create_shapefile_with_attributes(points, file_name, attributes, spatial_reference, output_folder)
            else:
                arcpy.AddWarning("No valid points extracted for land with CADGENNO: {}".format(cadgenno))
        for building in root.findall('.//Building'):
            building_id = building.find('BUILDINGID').text if building.find('BUILDINGID') is not None else "Unknown"
            land_id = building.find('LANDID').text if building.find('LANDID') is not None else "Unknown"
            cadgenno = building.find('CADGENNO').text if building.find('CADGENNO') is not None else "Unknown"
            cadgenno_clean = cadgenno.replace('-', '_')
            attributes = {
                'SIRSUP': ('TEXT', 50, sirsups),
                'ID_IMOBIL': ('TEXT', 50, land_cadgenno_mapping.get(land_id, "Unknown")),
                'COD_CTIE': ('TEXT', 50, cadgenno_clean.split('_')[1] if '_' in cadgenno_clean else cadgenno_clean)
            }
            points = [(pt.find('X').text, pt.find('Y').text) for pt in root.findall('.//Points[BUILDINGID="{}"]'.format(building_id))]
            if points:
                file_name = "{}.shp".format(cadgenno_clean)
                create_shapefile_with_attributes(points, file_name, attributes, spatial_reference, output_folder)
            else:
                arcpy.AddWarning("No valid points extracted for building with CADGENNO: {}".format(cadgenno_clean))
    arcpy.AddMessage("Processing complete. Check output folder for shapefiles.")
if __name__ == '__main__':
    input_folder = arcpy.GetParameterAsText(0)
    output_folder = arcpy.GetParameterAsText(1)
    main(input_folder, output_folder)
