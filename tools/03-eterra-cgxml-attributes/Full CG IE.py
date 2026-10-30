import arcpy
import os
import xml.etree.ElementTree as ET
def truncate_text(value, max_length):
    if value is None:
        return "None"
    return value[:max_length] if len(value) > max_length else value
def create_shapefile_with_attributes(points_list, attributes, spatial_ref, output_fc, ids_seen):
    if not points_list:
        arcpy.AddWarning("No points provided. Skipping...")
        return
    id_value = attributes.get("ID", [None, None, "None"])[2]
    if id_value in ids_seen:
        arcpy.AddWarning("Warning: ID {} is duplicated.".format(id_value))
    else:
        ids_seen.add(id_value)
    for field_name, field_info in attributes.items():
        if field_name not in [f.name for f in arcpy.ListFields(output_fc)]:
            arcpy.AddField_management(output_fc, field_name, field_info[0], field_length=field_info[1])
    cursor = arcpy.da.InsertCursor(output_fc, ['SHAPE@'] + list(attributes.keys()))
    array = arcpy.Array([arcpy.Point(float(x), float(y)) for x, y in points_list])
    polygon = arcpy.Polygon(array, spatial_ref)
    array.removeAll()
    try:
        truncated_attributes = [truncate_text(attr[2], attr[1]) if attr[0] == 'TEXT' else attr[2] for attr in attributes.values()]
        cursor.insertRow([polygon] + truncated_attributes)
    except Exception as e:
        arcpy.AddWarning("Failed to insert record: {}".format(e))
    finally:
        del cursor
def main(input_folder, output_file):
    arcpy.env.workspace = input_folder
    arcpy.env.overwriteOutput = True
    spatial_reference = arcpy.SpatialReference(31700)
    if arcpy.Exists(output_file):
        arcpy.Delete_management(output_file)
    merged_fc = arcpy.CreateFeatureclass_management(
        "in_memory", "merged", "POLYGON", spatial_reference=spatial_reference
    )
    ids_seen = set()
    cgxml_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.cgxml')]
    arcpy.AddMessage("Found {} CGXML file(s).".format(len(cgxml_files)))
    for file in cgxml_files:
        file_path = os.path.join(input_folder, file)
        arcpy.AddMessage("Processing file: {}".format(file_path))
        tree = ET.parse(file_path)
        root = tree.getroot()
        siruta = root.find('.//SIRUTA').text if root.find('.//SIRUTA') is not None else "None"
        sirsups = root.find('.//SIRSUP').text if root.find('.//SIRSUP') is not None else "None"
        intr_extr = root.find('.//INTRAVILAN').text if root.find('.//INTRAVILAN') is not None else "None"
        registrations = root.findall('.//Registration')
        deeds = root.findall('.//Deed')
        persons = root.findall('.//Person')
        parcels = root.findall('.//Parcel')
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None and land.find('LANDID').text is not None else "None"
            e2identifier = land.find('E2IDENTIFIER').text if land.find('E2IDENTIFIER') is not None else "None"
            measured_area = land.find('MEASUREDAREA').text if land.find('MEASUREDAREA') is not None else "None"
            legal_area = land.find('PARCELLEGALAREA').text if land.find('PARCELLEGALAREA') is not None else "None"
            is_new = land.find('ISNEW').text if land.find('ISNEW') is not None else "None"
            enclosed = land.find('ENCLOSED').text if land.find('ENCLOSED') is not None else "None"
            sector = land.find('CADSECTOR').text if land.find('CADSECTOR') is not None else "None"
            obs_imobil = land.find('NOTES').text if land.find('NOTES') is not None else "None"
            sup_mas_p = ", ".join([p.find('MEASUREDAREA').text if (p.find('MEASUREDAREA') is not None and p.find('MEASUREDAREA').text is not None) else "None" for p in parcels])
            folosinta = ", ".join([p.find('USECATEGORY').text if (p.find('USECATEGORY') is not None and p.find('USECATEGORY').text is not None) else "None" for p in parcels])
            intr_extr_p = ", ".join([p.find('INTRAVILAN').text if (p.find('INTRAVILAN') is not None and p.find('INTRAVILAN').text is not None) else "None" for p in parcels])
            titlu_p = ", ".join([p.find('TITLENO').text if (p.find('TITLENO') is not None and p.find('TITLENO').text is not None) else "None" for p in parcels])
            tarla = ", ".join([p.find('LANDPLOTNO').text if (p.find('LANDPLOTNO') is not None and p.find('LANDPLOTNO').text is not None) else "None" for p in parcels])
            parcela = ", ".join([p.find('PARCELNO').text if (p.find('PARCELNO') is not None and p.find('PARCELNO').text is not None) else "None" for p in parcels])
            deed_numbers = ", ".join([d.find('DEEDNUMBER').text if (d.find('DEEDNUMBER') is not None and d.find('DEEDNUMBER').text is not None) else "None" for d in deeds])
            deed_types = ", ".join([d.find('DEEDTYPE').text if (d.find('DEEDTYPE') is not None and d.find('DEEDTYPE').text is not None) else "None" for d in deeds])
            authorities = ", ".join([d.find('AUTHORITY').text if (d.find('AUTHORITY') is not None and d.find('AUTHORITY').text is not None) else "None" for d in deeds])
            tip_inscr = ", ".join([r.find('REGISTRATIONTYPE').text if (r.find('REGISTRATIONTYPE') is not None and r.find('REGISTRATIONTYPE').text is not None) else "None" for r in registrations])
            obs_ins = ", ".join([r.find('NOTES').text if (r.find('NOTES') is not None and r.find('NOTES').text is not None) else "None" for r in registrations])
            titlu_ins = ", ".join([r.find('TITLE').text if (r.find('TITLE') is not None and r.find('TITLE').text is not None) else "None" for r in registrations])
            cota = ", ".join([r.find('QUOTATYPE').text if (r.find('QUOTATYPE') is not None and r.find('QUOTATYPE').text is not None) else "None" for r in registrations])
            parte = ", ".join([r.find('LBPARTNO').text if (r.find('LBPARTNO') is not None and r.find('LBPARTNO').text is not None) else "None" for r in registrations])
            prenume = ", ".join([p.find('FIRSTNAME').text if (p.find('FIRSTNAME') is not None and p.find('FIRSTNAME').text is not None) else "None" for p in persons])
            nume = ", ".join([p.find('LASTNAME').text if (p.find('LASTNAME') is not None and p.find('LASTNAME').text is not None) else "None" for p in persons])
            mort = ", ".join([p.find('DEFUNCT').text if (p.find('DEFUNCT') is not None and p.find('DEFUNCT').text is not None) else "None" for p in persons])
            points = [
                (pt.find('X').text, pt.find('Y').text) 
                for pt in root.findall('.//Points[IMMOVABLEID="{}"]'.format(land_id))
                if pt.find('X') is not None and pt.find('Y') is not None
            ]
            attributes = {
                'ID': ('TEXT', 50, e2identifier),
                'SIRSUP': ('TEXT', 50, sirsups),
                'Siruta': ('TEXT', 50, siruta),
                'IntrExtr': ('TEXT', 50, intr_extr),
                'Sector': ('TEXT', 50, sector),
                'Sup_Mas': ('TEXT', 50, measured_area),
                'Sup_Acte': ('TEXT', 50, legal_area),
                'Nou': ('TEXT', 50, is_new),
                'Imprejmuit': ('TEXT', 50, enclosed),
                'SupMasP': ('TEXT', 250, sup_mas_p),
                'Folosinta': ('TEXT', 250, folosinta),
                'IntrExtrP': ('TEXT', 250, intr_extr_p),
                'TitluP': ('TEXT', 250, titlu_p),
                'Tarla': ('TEXT', 250, tarla),
                'Parcela': ('TEXT', 250, parcela),
                'Nr_Act': ('TEXT', 250, deed_numbers),
                'Tip_Act': ('TEXT', 250, deed_types),
                'Autoritate': ('TEXT', 250, authorities),
                'Tip_Inscr': ('TEXT', 250, tip_inscr),
                'Obs_Ins': ('TEXT', 250, obs_ins),
                'Titlu_Ins': ('TEXT', 250, titlu_ins),
                'Cota': ('TEXT', 250, cota),
                'Parte': ('TEXT', 250, parte),
                'Prenume': ('TEXT', 250, prenume),
                'Nume': ('TEXT', 250, nume),
                'Mort': ('TEXT', 50, mort),
                'Obs_Imobil': ('TEXT', 250, obs_imobil)
            }
            if points:
                create_shapefile_with_attributes(points, attributes, spatial_reference, merged_fc, ids_seen)
            else:
                arcpy.AddWarning("No geometry found for: {}".format(file))
    arcpy.CopyFeatures_management(merged_fc, output_file)
    arcpy.AddMessage("Merged shapefile created: {}".format(output_file))
if __name__ == '__main__':
    input_folder = arcpy.GetParameterAsText(0)
    output_file = arcpy.GetParameterAsText(1)
    main(input_folder, output_file)