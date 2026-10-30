import os
import shutil
import pandas as pd
sheet_name = input("Enter the Excel sheet name: ").strip()
# Set these paths before running
pdf_folder_path = r'C:\path\to\PDF init'
excel_file_path = r'C:\path\to\pdf_list.xlsx'
new_folder_path = r'C:\path\to\Renamed_PDFs'
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
df = pd.read_excel(excel_file_path, sheet_name=sheet_name, dtype={'pdf': str, 'ID': str, 'NR CF': str})
df.columns = df.columns.str.strip()
matched_files = []
unmatched_files = []
def generate_name_variations(base_name):
    base_name = base_name.replace('/', '-')
    parts = base_name.split('-')
    if len(parts) == 2:
        left, right = parts[0].strip(), parts[1].strip()
        variations = [
            f"{left}-{right}.pdf",
            f"{left} -{right}.pdf",
            f"{left}- {right}.pdf",
            f"{left} - {right}.pdf"
        ]
    else:
        variations = [f"{base_name}.pdf"]
    return variations
for index, row in df.iterrows():
    if pd.isna(row['pdf']) or pd.isna(row['ID']):
        continue
    pdf_name_from_excel = row['pdf']
    nr_cf_value = row['NR CF'] if not pd.isna(row['NR CF']) else None
    if nr_cf_value:
        new_name = f"{row['ID']}_{nr_cf_value}.pdf"
    else:
        new_name = f"{row['ID']}.pdf"
    variations = generate_name_variations(pdf_name_from_excel)
    file_found = False
    for variation in variations:
        original_path = os.path.join(pdf_folder_path, variation)
        if os.path.exists(original_path):
            new_path = os.path.join(new_folder_path, new_name)
            shutil.copy(original_path, new_path)
            matched_files.append(variation)
            file_found = True
            break
    if not file_found:
        unmatched_files.append(pdf_name_from_excel)
print("The folder has been created.")