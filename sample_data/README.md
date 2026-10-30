# Sample data

Fictional data for trying every tool in this repository.

## How it was made

The files were built from the structure of real CGXML files, so they behave like the real thing: neighbouring properties with houses and annexes, several owners with shares, a deceased owner, an unidentified owner, notes and legal registrations. Then everything that could point to a real person, property or place was replaced:

* names of owners, notaries and officials (notaries now appear as BNP EXEMPLU 1 to 6)
* personal ID numbers (CNP) and company ID numbers
* addresses, postal numbers and administrative unit codes
* land book, cadastral, title, deed, application and tarla or parcel numbers
* dates and issuing authorities
* descriptions of buildings (years and floor areas)
* coordinates: every parcel was moved far from its real position, so the shapes and areas stay correct but the location is not real

Fictional personal ID numbers have zeros where the birth date would be, so they can never belong to a real person. Only public references were kept as they are, such as Law 7/1996 and ANCPI Order 634/2006.

**Do not use this data for anything real.**

## What is here

| Folder | Content | Used by |
|--------|---------|---------|
| `eterra_cgxml` | 13 CGXML files in the e-Terra download format (IDs 50101 to 50113), 13 neighbouring properties with 17 buildings. | Tools 01, 03, helper `Separare.py` |
| `generare_cg_cgxml` | 13 CGXML files in the Generare CG format (IDs 101 to 113), including an unidentified owner, a property with several parcels and one with a building. | Tools 07, 08, 10 and the XML helpers |
| `shapefiles` | `Land` and `Buildings` (merged layers, as tools 01 and 02 produce them), `Imobile`, `ID_Imobile`, `Constructii` and `Nr_Constructii` (drawing style inputs with text labels), and `Intravilan_limit` (a built up area limit). Stereo 70 (EPSG:31700). | Tools 05, 06, 09 |
| `rename_pdfs` | 8 sample PDFs named the way scans usually arrive, and `pdf_list.xlsx` that links them to IDs. | Tool 04 |
| `excel_to_cgxml` | `parcels.xlsx`, a parcel table with 4 properties. | Tool 11 |
