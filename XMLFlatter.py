import os
import warnings
import argparse
import xml.etree.ElementTree as ET
import csv
from tqdm import tqdm # type: ignore

# Define all arguments available
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder_path", help="The folder containing the XML files.", required=True)
parser.add_argument("-o", "--output_file", help="The CSV file where all data will be stored.", required=True)
parser.add_argument("-e", "--extension", help="Specify the extension of the files that need to be flattened.")
parser.add_argument("--suppress-warnings", action="store_true", help="Suppress warning messages.")
args = parser.parse_args()

# Get all arguments
folder_path = args.folder_path
output_file = args.output_file
extension = args.extension
suppress_warnings = args.suppress_warnings

# Suppress warnings if the flag is set
if suppress_warnings:
    warnings.filterwarnings("ignore")
else:
    warnings.simplefilter("always")

# Check if all required arguments were given
if folder_path is None or output_file is None:
    print("Not enough data was given, use -h to see all arguments.")
    exit()

# Format output_file so that it ends with .csv
if not output_file.endswith('.csv'):
    output_file += '.csv'

# Get all files that end with the provided extension from the folder given
files = [f for f in os.listdir(folder_path) if extension is None or f.endswith(extension)]

# Initialize the rows and headers lists
rows = []
headers = []

# Start going through the files
for file_name in tqdm(files, desc="Processing files", unit="file"):
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
            headers.append(field_name)

    if 'FILENAME' not in headers:
        headers.append('FILENAME')

    if len(root[0][2]) == 1 :
        if len(root[0][2][0][1]) == 1:
            row['FILENAME'] = root[0][2][0][1][0].attrib['Path']

        else:
            warnings.warn(f"{file_name}: Renditions are either 0 or too many.")

    else:
        warnings.warn(f"{file_name}: Versions are either 0 or too many.")

    rows.append(row)

# Write all data collected in the given CSV file
with open(output_file, 'w', newline = '', encoding = "utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = headers, delimiter = ';')
    writer.writeheader()
    for row in rows:
        writer.writerow({header: row.get(header, "") for header in headers})