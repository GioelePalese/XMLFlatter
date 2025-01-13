import os
import argparse
import xml.etree.ElementTree as ET
import csv

# Define all arguments available
parser = argparse.ArgumentParser()
parser.add_argument("-fp", "--folder_path", help="The folder containing the XML files.", required=True)
parser.add_argument("-op", "--output_file", help="The CSV file where all data will be stored.", required=True)
args = parser.parse_args()

# Get all arguments
folder_path = args.folder_path
output_file = args.output_file

# Check if all required arguments were given
if folder_path is None or output_file is None:
    print("Not enough data was given, use -h to see all arguments.")
    exit()

# Format output_file so that it ends with .csv
if not output_file.endswith('.csv'):
    output_file += '.csv'

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
with open(output_file, 'w', newline = '', encoding = "utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = ';')
    writer.writeheader()
    for row in rows:
        writer.writerow({header: row.get(header, "") for header in headers})