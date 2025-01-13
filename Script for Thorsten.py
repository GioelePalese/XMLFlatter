import os
import xml.etree.ElementTree as ET
import csv

# Ask for the folder path where data has to be read from and the path for the file where everything will be saved
folder_path = input ( "Folder Path: " )
output_csv_path  = input ( "CSV Path: " )

# Get all files that end with .dms1importbatch from the folder given
files = [f for f in os.listdir(folder_path) if f.endswith('.dms1importbatch')]

# Initialize the rows and headers lists
rows = []
headers = []

# Start going through the files
for file_name in files:
    # Read file
    tree = ET.parse(os.path.join(folder_path, file_name))
    root = tree.getroot()

    # Save all IndexDataItem values in the rows list and all the different types of field names in headers
    row = {}
    for item in root[0][1]:
        field_name = item.attrib['FieldName']
        field_value = item.text or ""

        row[field_name] = field_value

        if field_name not in headers:
            headers.append(item.attrib['FieldName'])
        
    rows.append(row)

# Write all data collected in the given CSV file
with open(output_csv_path, 'w', newline = '', encoding = "utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = ';')
    writer.writeheader()
    for row in rows:
        writer.writerow({header: row.get(header, "") for header in headers})