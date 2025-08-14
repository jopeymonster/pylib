import csv
import os
import datetime
from urllib.parse import urlparse
import argparse

menu_message = (
    "XML File Converter by JDT\n"
    "Current capabilities: Convert CSV files into XML\n"
    " - Provide a CSV file containing a list of URLs and generate a basic XML sitemap file\n"
)

def validate_file_path(file_path):
    return os.path.exists(file_path)

def generate_xml_row(loc, changefreq=None, priority=None):
    xml_row = f"<url>\n  <loc>{loc}</loc>\n"
    if changefreq:
        xml_row += f"  <changefreq>{changefreq}</changefreq>\n"
    if priority:
        xml_row += f"  <priority>{priority}</priority>\n"
    xml_row += "</url>\n"
    return xml_row

def convert_csv_to_xml(csv_file, filename_input=None):
    """Convert CSV file to XML sitemap."""
    if filename_input:
        xml_file_name = f"{filename_input}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"
    else:
        xml_file_name = f"xml_file_output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(xml_file_name, 'w', encoding='utf-8') as xmlfile:
            xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            xmlfile.write('<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for row_number, row in enumerate(reader, start=2):
                loc = row.get('loc', '').strip()
                changefreq = row.get('changefreq', '').strip()
                priority = row.get('priority', '').strip()
                if not all([loc, changefreq, priority]):
                    print(f"ERROR: Missing XML data in row {row_number}")
                    continue
                parsed = urlparse(loc)
                if not parsed.scheme or not parsed.netloc:
                    print(f"ERROR: Invalid URL in row {row_number}: {loc}")
                    continue
                xmlfile.write(generate_xml_row(loc, changefreq, priority))
            xmlfile.write('</urlset>\n')
    print("Conversion completed successfully.\n"
          f"Data saved to {os.path.abspath(xml_file_name)}")

def main():
    parser = argparse.ArgumentParser(
        prog="Simple CSV to XML File Converter",
        description="Provide a CSV file in the proper format with 'loc', 'changefreq', and 'priority' node values.",
        epilog="Developed by JDT",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--input", help="Full path to the CSV file to convert.")
    parser.add_argument("--output", help="Base name for the output XML file (without extension).")
    args = parser.parse_args()
    # CSV path
    csv_file = args.input
    if not csv_file:
        print(menu_message)
        csv_file = input("Enter the path to the CSV file: ").strip()
        while not validate_file_path(csv_file):
            print("Invalid file path. Please enter a valid path.")
            csv_file = input("Enter the path to the CSV file: ").strip()
    # output filename
    filename_input = args.output
    if not filename_input:
        filename_input = input("Enter the name for the output XML file (Press Enter for default): ").strip()
        if not filename_input:
            filename_input = None  # default convert_csv_to_xml()
    convert_csv_to_xml(csv_file, filename_input)

if __name__ == "__main__":
    main()
