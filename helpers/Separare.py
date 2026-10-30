import os
import pandas as pd
import numpy
def compare_folders(cgxml_folder_path, shp_folder_path, output_excel_path):
    cgxml_files = {os.path.splitext(f)[0] for f in os.listdir(cgxml_folder_path) if f.endswith('.cgxml')}
    shp_files = {os.path.splitext(f)[0] for f in os.listdir(shp_folder_path) if f.endswith('.shp')}
    common_files = sorted(cgxml_files.intersection(shp_files))
    unique_files = sorted(cgxml_files.symmetric_difference(shp_files))
    data = {
        "File Name in Both Folders": common_files + [''] * (len(unique_files) - len(common_files)),
        "File Name Not in Both Folders": unique_files + [''] * (len(common_files) - len(unique_files))
    }
    df = pd.DataFrame(data)
    df.to_excel(output_excel_path, index=False, sheet_name="Comparison")
    print(f"Excel file created at {output_excel_path}")
# Set these paths before running
cgxml_folder = r"C:\path\to\CGXML_folder"
shp_folder = r"C:\path\to\SHP_folder"
output_excel = r"C:\path\to\comparison.xlsx"
compare_folders(cgxml_folder, shp_folder, output_excel)
