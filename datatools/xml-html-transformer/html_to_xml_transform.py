# excludes lastmod element field
# dev: handle invalid urls

import csv
import os
import datetime

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

def convert_csv_to_xml(csv_file, xml_file_name=None):
    if not xml_file_name:
        xml_file_name = f"xml_file_output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"
    else:
        xml_file_name = f"{xml_file_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile: 
        reader = csv.DictReader(csvfile)
        next(reader) 
        with open(xml_file_name, 'w') as xmlfile:
            xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            xmlfile.write('<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for row in reader:
                loc = row.get('loc')
                changefreq = row.get('changefreq')
                priority = row.get('priority')
                xmlfile.write(generate_xml_row(loc, changefreq, priority))
            xmlfile.write('</urlset>\n')

def main():
    csv_file_path = input("Enter the path to the CSV file: ")
    while not validate_file_path(csv_file_path):
        print("Invalid file path. Please enter a valid path.")
        csv_file_path = input("Enter the path to the CSV file: ")

    xml_file_name = input("Enter the name for the output XML file (Press Enter for default): ").strip()
    convert_csv_to_xml(csv_file_path, xml_file_name)
    print("Conversion completed successfully.")

if __name__ == "__main__":
    main()