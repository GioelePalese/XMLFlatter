![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

## About
This project is used for flattening a folder full of XML files into a single csv file with all IndexDataItems saved in their proper columns.

## Usage

```batch
py .\XMLFlatter.py
```

### Flags
#### Required:
- -f, --folder_path : The folder containing the XML files.
- -o, --output_path : The CSV file where all data will be stored.
#### Optional:
- -e, --extension : Specify the extension of the files that need to be flattened.
