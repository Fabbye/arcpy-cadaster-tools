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
        if check_and_update_land(root):
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print("Updated file: {}".format(file_path))
        else:
            print("No updates needed for: {}".format(file_path))
    except Exception as e:
        print("Error processing file {}: {}".format(file_path, e))
def check_and_update_land(root):
    updated = False
    for land in root.findall(".//Land"):
        measured_area = land.find("MEASUREDAREA")
        parcel_legal_area = land.find("PARCELLEGALAREA")
        if parcel_legal_area is None and measured_area is not None:
            parcel_legal_area = ET.Element("PARCELLEGALAREA")
            parcel_legal_area.text = "0"
            land_children = list(land)
            for i, child in enumerate(land_children):
                if child.tag == "MEASUREDAREA":
                    land.insert(i + 1, parcel_legal_area)
                    updated = True
                    break
    return updated
# Set this path before running
folder_path = r"C:\path\to\CGXML_folder"
process_folder(folder_path)
