import arcpy
import os
import xml.etree.ElementTree as ET
import sys
if sys.version_info[0] < 3:  # Python 2
    text_type = unicode
else:
    text_type = str
def truncate_text(value, max_length):
    if value is None:
        return "Unknown"
    return value[:max_length] if len(value) > max_length else value
def create_shapefile_with_attributes(points_list, attributes, spatial_ref, output_fc, ids_seen):
    if not points_list:
        arcpy.AddWarning("No points provided. Skipping...")
        return
    id_value = attributes.get("ID", [None, None, "Unknown"])[2]
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
def extract_parcel_info(parcels):
    parcel_nos = []
    land_plot_nos = []
    use_categories = []
    for parcel in parcels:
        parcel_no = parcel.find('PARCELNO').text if parcel.find('PARCELNO') is not None else "Unknown"
        land_plot_no = parcel.find('LANDPLOTNO').text if parcel.find('LANDPLOTNO') is not None else "Unknown"
        use_category = parcel.find('USECATEGORY').text if parcel.find('USECATEGORY') is not None else "Unknown"
        parcel_nos.append(text_type(parcel_no))
        land_plot_nos.append(text_type(land_plot_no))
        use_categories.append(text_type(use_category))
    return ", ".join(parcel_nos), ", ".join(land_plot_nos), ", ".join(use_categories)
def extract_deed_info(deeds):
    deed_ids = []
    deed_numbers = []
    deed_dates = []
    deed_types = []
    authorities = []
    deed_notes = []
    for deed in deeds:
        deed_id = deed.find('DEEDID').text if deed.find('DEEDID') is not None else "Unknown"
        deed_number = deed.find('DEEDNUMBER').text if deed.find('DEEDNUMBER') is not None else "Unknown"
        deed_date = deed.find('DEEDDATE').text if deed.find('DEEDDATE') is not None else "Unknown"
        if "T" in deed_date:
            deed_date = deed_date.split("T")[0]
        deed_type = deed.find('DEEDTYPE').text if deed.find('DEEDTYPE') is not None else "Unknown"
        authority = deed.find('AUTHORITY').text if deed.find('AUTHORITY') is not None else "Unknown"
        deed_note = deed.find('NOTES').text if deed.find('NOTES') is not None else "Unknown"
        deed_ids.append(text_type(deed_id))
        deed_numbers.append(text_type(deed_number))
        deed_dates.append(text_type(deed_date))
        deed_types.append(text_type(deed_type))
        authorities.append(text_type(authority))
        deed_notes.append(text_type(deed_note))
    return (
        ", ".join(deed_ids),
        ", ".join(deed_numbers),
        ", ".join(deed_dates),
        ", ".join(deed_types),
        ", ".join(authorities),
        ", ".join(deed_notes),
    )
def extract_person_info(persons):
    person_ids = []
    address_ids = []
    first_names = []
    last_names = []
    defuncts = []
    identifieds = []
    idcodes = []
    notes = []
    for person in persons:
        person_id = person.find('PERSONID').text if person.find('PERSONID') is not None else "Unknown"
        address_id = person.find('ADDRESSID').text if person.find('ADDRESSID') is not None else "Unknown"
        first_name = person.find('FIRSTNAME').text if person.find('FIRSTNAME') is not None else "Unknown"
        last_name = person.find('LASTNAME').text if person.find('LASTNAME') is not None else "Unknown"
        defunct = person.find('DEFUNCT').text if person.find('DEFUNCT') is not None else "Unknown"
        identified = person.find('IDENTIFIED').text if person.find('IDENTIFIED') is not None else "Unknown"
        idcode = person.find('IDCODE').text if person.find('IDCODE') is not None else "Unknown"
        note = person.find('NOTES').text if person.find('NOTES') is not None else "Unknown"
        person_ids.append(text_type(person_id))
        address_ids.append(text_type(address_id))
        first_names.append(text_type(first_name))
        last_names.append(text_type(last_name))
        defuncts.append(text_type(defunct))
        identifieds.append(text_type(identified))
        idcodes.append(text_type(idcode))
        notes.append(text_type(note))
    return (
        ", ".join(person_ids),
        ", ".join(address_ids),
        ", ".join(first_names),
        ", ".join(last_names),
        ", ".join(defuncts),
        ", ".join(identifieds),
        ", ".join(idcodes),
        ", ".join(notes),
    )
def extract_registration_info(registrations):
    reg_ids = []
    reg_types = []
    right_types = []
    right_comments = []
    act_regs = []
    titles = []
    quota_types = []
    actual_quotas = []
    quota_comments = []
    for reg in registrations:
        reg_id = reg.find('REGISTRATIONID').text if reg.find('REGISTRATIONID') is not None else "Unknown"
        reg_type = reg.find('REGISTRATIONTYPE').text if reg.find('REGISTRATIONTYPE') is not None else "Unknown"
        right_type = reg.find('RIGHTTYPE').text if reg.find('RIGHTTYPE') is not None else "Unknown"
        right_comment = reg.find('RIGHTCOMMENT').text if reg.find('RIGHTCOMMENT') is not None else "Unknown"
        act_reg = reg.find('DEEDID').text if reg.find('DEEDID') is not None else "Unknown"
        title = reg.find('TITLE').text if reg.find('TITLE') is not None else "Unknown"
        quota_type = reg.find('QUOTATYPE').text if reg.find('QUOTATYPE') is not None else "Unknown"
        actual_quota = reg.find('ACTUALQUOTA').text if reg.find('ACTUALQUOTA') is not None else "Unknown"
        quota_comment = reg.find('COMMENTS').text if reg.find('COMMENTS') is not None else "Unknown"
        reg_ids.append(text_type(reg_id))
        reg_types.append(text_type(reg_type))
        right_types.append(text_type(right_type))
        right_comments.append(text_type(right_comment))
        act_regs.append(text_type(act_reg))
        titles.append(text_type(title))
        quota_types.append(text_type(quota_type))
        actual_quotas.append(text_type(actual_quota))
        quota_comments.append(text_type(quota_comment))
    return (
        ", ".join(reg_ids),
        ", ".join(reg_types),
        ", ".join(right_types),
        ", ".join(right_comments),
        ", ".join(act_regs),
        ", ".join(titles),
        ", ".join(quota_types),
        ", ".join(actual_quotas),
        ", ".join(quota_comments),
    )
def determine_intr_extr_value(parcels):
    return any(parcel.find('INTRAVILAN') is not None and parcel.find('INTRAVILAN').text.lower() == 'true' for parcel in parcels)
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
        sirsups = root.find('.//SIRSUP').text if root.find('.//SIRSUP') is not None else "Unknown"
        parcels = root.findall('.//Parcel')
        intr_extr_value = determine_intr_extr_value(parcels)
        parcel_nos, land_plot_nos, use_categories = extract_parcel_info(parcels)
        deeds = root.findall('.//Deed')
        act_ids, numar_acts, data_acts, tip_acts, autoritati, obs_acts = extract_deed_info(deeds)
        persons = root.findall('.//Person')
        id_persons, id_pers_adrs, first_names, last_names, defuncts, identifieds, idcodes, obs_pers = extract_person_info(persons)
        registrations = root.findall('.//Registration')
        reg_ids, reg_types, right_types, right_comments, act_regs, titles, quota_types, actual_quotas, quota_comments = extract_registration_info(registrations)
        for land in root.findall('.//Land'):
            land_id = land.find('LANDID').text if land.find('LANDID') is not None else "Unknown"
            cadgenno = land.find('CADGENNO').text if land.find('CADGENNO') is not None else "Unknown"
            obs_imobil = land.find('NOTES').text if land.find('NOTES') is not None else "No Notes"
            measured_area = land.find('MEASUREDAREA').text if land.find('MEASUREDAREA') is not None else "Unknown"
            parcel_legal_area = land.find('PARCELLEGALAREA').text if land.find('PARCELLEGALAREA') is not None else "Unknown"
            cf_value = land.find('E2IDENTIFIER').text if land.find('E2IDENTIFIER') is not None else "Unknown"
            attributes = {
                'SIRSUP': ('TEXT', 50, sirsups),
                'ID': ('TEXT', 50, cadgenno),
                'SECTOR': ('TEXT', 50, land.find('CADSECTOR').text if land.find('CADSECTOR') is not None else "Unknown"),
                'IntrExtr': ('TEXT', 5, 'True' if intr_extr_value else "False"),
                'Obs_Imobil': ('TEXT', 250, obs_imobil),
                'Nr_Parcela': ('TEXT', 250, parcel_nos),
                'Tarla': ('TEXT', 250, land_plot_nos),
                'Folosinta': ('TEXT', 250, use_categories),
                'T_Sup_Mas': ('TEXT', 50, measured_area),
                'T_Sup_Act': ('TEXT', 50, parcel_legal_area),
                'Act_ID': ('TEXT', 250, act_ids),
                'Numar_Act': ('TEXT', 250, numar_acts),
                'Data_Act': ('TEXT', 50, data_acts),
                'Tip_Act': ('TEXT', 250, tip_acts),
                'Autoritate': ('TEXT', 250, autoritati),
                'Obs_Act': ('TEXT', 250, obs_acts),
                'ID_Person': ('TEXT', 250, id_persons),
                'IdPersAdr': ('TEXT', 250, id_pers_adrs),
                'Prenume': ('TEXT', 250, first_names),
                'Nume': ('TEXT', 250, last_names),
                'Mort': ('TEXT', 50, defuncts),
                'Identif': ('TEXT', 50, identifieds),
                'CNP': ('TEXT', 250, idcodes),
                'Obs_Pers': ('TEXT', 250, obs_pers),
                'ID_Regis': ('TEXT', 250, reg_ids),
                'Tip_Regis': ('TEXT', 250, reg_types),
                'DreptRegis': ('TEXT', 250, right_types),
                'Com_Regis': ('TEXT', 250, right_comments),
                'Act_Reg': ('TEXT', 250, act_regs),
                'Titlu_Reg': ('TEXT', 250, titles),
                'Tip_Cota': ('TEXT', 250, quota_types),
                'Val_Cota': ('TEXT', 250, actual_quotas),
                'Com_Cota': ('TEXT', 250, quota_comments),
                'CF': ('TEXT', 50, cf_value),
            }
            points = [(pt.find('X').text, pt.find('Y').text) for pt in root.findall('.//Points[IMMOVABLEID="{}"]'.format(land_id))]
            if points:
                create_shapefile_with_attributes(points, attributes, spatial_reference, merged_fc, ids_seen)
            else:
                arcpy.AddWarning("No valid points extracted for land with CADGENNO: {}".format(cadgenno))
    arcpy.CopyFeatures_management(merged_fc, output_file)
    arcpy.AddMessage("Merged shapefile created: {}".format(output_file))
if __name__ == '__main__':
    input_folder = arcpy.GetParameterAsText(0)
    output_file = arcpy.GetParameterAsText(1)
    main(input_folder, output_file)