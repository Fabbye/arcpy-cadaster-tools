import os
import pandas as pd
from lxml import etree
# Set this path before running
file_path = r'C:\path\to\parcels.xlsx'
sheet_name = 'Export Worksheet'
data = pd.read_excel(file_path, sheet_name=sheet_name)
required_columns = ['ID', 'Nr TP', 'Data TP', 'Categorie', 'Proprietari', 'Sup parcela', 'Intra/Extravilan']
for column in required_columns:
    if column not in data.columns:
        raise KeyError(f"Missing required column: {column}")
data['Categorie'] = data['Categorie'].fillna('1').astype(str).str.split(' - ').str[0]
data['Proprietari'] = data['Proprietari'].fillna('N/A')
data['Intra/Extravilan'] = data['Intra/Extravilan'].map({'I': 'true', 'E': 'false'}).fillna('false')
data['Data TP'] = pd.to_datetime(data['Data TP'], errors='coerce').dt.strftime('%Y-%m-%d').fillna('N/A')
# Set this path before running
output_folder = r'C:\path\to\CGXML_Output'
os.makedirs(output_folder, exist_ok=True)
def create_cgxml_file(group):
    print(f"Processing group with ID {group['ID'].iloc[0]}")
    root = etree.Element('CGXML')
    address = etree.SubElement(root, 'Address')
    etree.SubElement(address, 'ADDRESSID').text = '1'
    etree.SubElement(address, 'SIRSUP').text = '79932'
    etree.SubElement(address, 'SIRUTA').text = '79941'
    etree.SubElement(address, 'INTRAVILAN').text = group['Intra/Extravilan'].iloc[0]
    etree.SubElement(address, 'POSTALNUMBER').text = '10000'
    etree.SubElement(address, 'BLOCK').text = '1'
    etree.SubElement(address, 'ENTRY').text = '1'
    etree.SubElement(address, 'FLOOR').text = '1'
    etree.SubElement(address, 'APNO').text = '1'
    etree.SubElement(address, 'ZIPCODE').text = '999999'
    etree.SubElement(address, 'DESCRIPTION').text = 'N/A'
    etree.SubElement(address, 'SECTION').text = '1'
    land = etree.SubElement(root, 'Land')
    etree.SubElement(land, 'LANDID').text = '1'
    etree.SubElement(land, 'CADSECTOR').text = '1'
    etree.SubElement(land, 'ADDRESSID').text = '1'
    total_area = str(group['Sup parcela'].sum())
    etree.SubElement(land, 'MEASUREDAREA').text = total_area
    etree.SubElement(land, 'PARCELLEGALAREA').text = total_area
    etree.SubElement(land, 'ISNEW').text = 'true'
    etree.SubElement(land, 'NOTES').text = 'N/A'
    etree.SubElement(land, 'ENCLOSED').text = 'false'
    etree.SubElement(land, 'COAREA').text = 'true'
    etree.SubElement(land, 'E2IDENTIFIER').text = '1'
    etree.SubElement(land, 'PAPERCADNO').text = '1'
    etree.SubElement(land, 'PAPERLBNO').text = '1'
    etree.SubElement(land, 'TOPONO').text = '1'
    etree.SubElement(land, 'CADGENNO').text = str(group['ID'].iloc[0])
    deed = etree.SubElement(root, 'Deed')
    etree.SubElement(deed, 'DEEDID').text = '1'
    etree.SubElement(deed, 'DEEDNUMBER').text = str(int(group['Nr TP'].iloc[0])) if pd.notna(group['Nr TP'].iloc[0]) else ''
    etree.SubElement(deed, 'DEEDDATE').text = group['Data TP'].iloc[0]
    etree.SubElement(deed, 'DEEDTYPE').text = 'ADMINISTRATIVE_1'
    etree.SubElement(deed, 'AUTHORITY').text = 'CJPSDPAT GORJ'
    etree.SubElement(deed, 'NOTES').text = 'N/A'
    etree.SubElement(deed, 'FILEID').text = '1'
    parcel_id = 1
    for _, row in group.iterrows():
        parcel = etree.SubElement(root, 'Parcel')
        etree.SubElement(parcel, 'PARCELID').text = str(parcel_id)
        parcel_id += 1
        etree.SubElement(parcel, 'LANDID').text = '1'
        etree.SubElement(parcel, 'NUMBER').text = '1'
        etree.SubElement(parcel, 'MEASUREDAREA').text = str(row['Sup parcela'])
        etree.SubElement(parcel, 'USECATEGORY').text = row['Categorie']
        etree.SubElement(parcel, 'INTRAVILAN').text = row['Intra/Extravilan']
        etree.SubElement(parcel, 'TITLENO').text = str(int(group['Nr TP'].iloc[0])) if pd.notna(group['Nr TP'].iloc[0]) else ''
        etree.SubElement(parcel, 'LANDPLOTNO').text = str(row['Tarla']) if 'Tarla' in row else ''  # Add Tarla if exists
        etree.SubElement(parcel, 'PARCELNO').text = str(row['Parcela']) if 'Parcela' in row and pd.notna(row['Parcela']) else ''  # Parcela rule
        etree.SubElement(parcel, 'NOTES').text = 'N/A'
        etree.SubElement(parcel, 'TOPONO').text = '1'
        etree.SubElement(parcel, 'CADGENNO').text = str(group['ID'].iloc[0])
    registration = etree.SubElement(root, 'Registration')
    etree.SubElement(registration, 'REGISTRATIONID').text = '1'
    etree.SubElement(registration, 'REGISTRATIONTYPE').text = 'INTAB'
    etree.SubElement(registration, 'RIGHTTYPE').text = 'PROPRIETATE'
    etree.SubElement(registration, 'RIGHTCOMMENT').text = 'titlu drept de reconstituire'
    etree.SubElement(registration, 'DEEDID').text = '1'
    etree.SubElement(registration, 'TITLE').text = 'LEGE'
    etree.SubElement(registration, 'QUOTATYPE').text = 'FRACTION_QUOTA'
    etree.SubElement(registration, 'ACTUALQUOTA').text = '1/1'
    etree.SubElement(registration, 'COMMENTS').text = 'No comments'
    etree.SubElement(registration, 'LBPARTNO').text = '2'
    etree.SubElement(registration, 'POSITION').text = '1'
    person_id = 1
    for name in group['Proprietari'].iloc[0].split(' / '):
        person = etree.SubElement(root, 'Person')
        etree.SubElement(person, 'PERSONID').text = str(person_id)
        person_id += 1
        etree.SubElement(person, 'ADDRESSID').text = '1'
        etree.SubElement(person, 'FIRSTNAME').text = name.strip()
        etree.SubElement(person, 'ISPHYSICAL').text = 'true'
        etree.SubElement(person, 'LASTNAME').text = name.strip()
        etree.SubElement(person, 'DEFUNCT').text = 'false'
        etree.SubElement(person, 'IDENTIFIED').text = 'true'
        etree.SubElement(person, 'NOTES').text = 'N/A'
        etree.SubElement(person, 'REGISTRATIONID').text = '1'
    file_name = os.path.join(output_folder, f"{group['ID'].iloc[0]}.cgxml")
    with open(file_name, 'wb') as file:
        tree = etree.ElementTree(root)
        tree.write(file, pretty_print=True, xml_declaration=True, encoding='UTF-8')
for _, group in data.groupby('ID'):
    create_cgxml_file(group)
print(f"CGXML files have been generated in the '{output_folder}' folder.")
