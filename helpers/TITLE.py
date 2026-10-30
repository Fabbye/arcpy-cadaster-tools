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
        if ensure_title_after_deedid(root):
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            print("Updated file: {}".format(file_path))
        else:
            print("No updates needed for: {}".format(file_path))
    except Exception as e:
        print("Error processing file {}: {}".format(file_path, e))
def ensure_title_after_deedid(root):
    updated = False
    for registration in root.findall(".//Registration"):
        deedid_index = None
        for i, element in enumerate(list(registration)):
            if element.tag == "DEEDID":
                deedid_index = i
                break
        if deedid_index is not None:
            siblings = list(registration)
            if len(siblings) <= deedid_index + 1 or siblings[deedid_index + 1].tag != "TITLE":
                title_element = ET.Element("TITLE")
                registration.insert(deedid_index + 1, title_element)
                updated = True
    return updated
# Set this path before running
path_to_folder = r"C:\path\to\CGXML_folder"
process_folder(path_to_folder)
