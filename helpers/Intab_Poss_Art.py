import os
import xml.etree.ElementTree as ET
def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("Invalid folder path: {}".format(folder_path))
        return
    for filename in os.listdir(folder_path):
        if filename.endswith(".CGXML"):
            file_path = os.path.join(folder_path, filename)
            process_file(file_path)
def process_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        if check_and_update_conditions(root):
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print("Updated file: {}".format(file_path))
        else:
            print("No updates needed for: {}".format(file_path))
    except Exception as e:
        print("Error processing file {}: {}".format(file_path, e))
def check_and_update_conditions(root):
    updated = False
    deedid_to_deednumber7 = {}
    for deed in root.findall(".//Deed"):
        deed_id = deed.find("DEEDID")
        deed_number = deed.find("DEEDNUMBER")
        deed_type = deed.find("DEEDTYPE")
        if deed_id is not None and deed_number is not None:
            deedid_to_deednumber7[deed_id.text] = (deed_number.text == "7")
            if deed_number.text == "7":
                if deed_type is None:
                    deed_type = ET.Element("DEEDTYPE")
                    deed.append(deed_type)
                if deed_type.text != "ACT_NORMATIV":
                    deed_type.text = "ACT_NORMATIV"
                    updated = True
        notes = deed.find("NOTES")
        if notes is None:
            notes = ET.Element("NOTES")
            deed.append(notes)
        if notes.text != "art.13, alin.14, alin.15":
            notes.text = "art.13, alin.14, alin.15"
            updated = True
    regid_to_neidentificat = {}
    for person in root.findall(".//Person"):
        reg_id = person.find("REGISTRATIONID")
        firstname = person.find("FIRSTNAME")
        if reg_id is not None and firstname is not None and firstname.text == "NEIDENTIFICAT":
            regid_to_neidentificat[reg_id.text] = True
    for registration in root.findall(".//Registration"):
        reg_deedid = registration.find("DEEDID")
        reg_regid = registration.find("REGISTRATIONID")
        reg_type = registration.find("REGISTRATIONTYPE")
        if reg_deedid is not None and deedid_to_deednumber7.get(reg_deedid.text, False):
            if reg_type is not None and reg_type.text == "INTAB":
                reg_type.text = "POSESION_REGISTATION"
                ensure_registration_attributes(registration)
                updated = True
        if (
            reg_regid is not None
            and reg_type is not None
            and reg_regid.text in regid_to_neidentificat
            and reg_type.text == "NOTATION"
        ):
            notes = registration.find("NOTES")
            if notes is None:
                notes = ET.Element("NOTES")
                registration.append(notes)
            notes.text = "se noteaza mentiunea de proprietar neidentificat"
            updated = True
    return updated
def ensure_registration_attributes(registration):
    righttype = registration.find("RIGHTTYPE")
    if righttype is None:
        righttype = ET.Element("RIGHTTYPE")
        registration.append(righttype)
    righttype.text = "PROPRIETATE"
    title = registration.find("TITLE")
    if title is None:
        title = ET.Element("TITLE")
        registration.append(title)
    title.text = "LEGE"
    quotatype = registration.find("QUOTATYPE")
    if quotatype is None:
        quotatype = ET.Element("QUOTATYPE")
        registration.append(quotatype)
    quotatype.text = "FRACTION_QUOTA"
    actualquota = registration.find("ACTUALQUOTA")
    if actualquota is None:
        actualquota = ET.Element("ACTUALQUOTA")
        registration.append(actualquota)
    actualquota.text = "1/1"
# Set this path before running
folder_path = r"C:\path\to\CGXML_folder"
process_folder(folder_path)
