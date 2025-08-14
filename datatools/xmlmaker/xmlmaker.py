import csv
import os
import datetime
from urllib.parse import urlparse
import argparse

menu_message = (
    "XML File Converter by JDT\n"
    "Current capabilities:\n"
    " - Convert formatted CSV (loc, changefreq, priority) into XML\n"
    " - Convert CSV with only loc column — auto-fill changefreq/priority\n"
    " - Convert CSV with no header (single URL column) — auto-fill changefreq/priority\n"
    " - Convert TXT file (one URL per line) — auto-fill changefreq/priority\n"
    " - Automatically removes duplicate URLs\n"
)

def validate_file_path(file_path):
    return os.path.exists(file_path)

def generate_priority(loc):
    """Generate priority value based on URL patterns."""
    loc_lower = loc.lower()
    if "catpage" in loc_lower:
        return "0.8"
    elif "lc" in loc_lower:
        return "0.9"
    elif "videovault" in loc_lower:
        return "0.7"
    elif "supportcenter" in loc_lower:
        return "0.5"
    return "1.0"

def generate_xml_row(loc, changefreq=None, priority=None):
    xml_row = f"<url>\n  <loc>{loc}</loc>\n"
    if changefreq:
        xml_row += f"  <changefreq>{changefreq}</changefreq>\n"
    if priority:
        xml_row += f"  <priority>{priority}</priority>\n"
    xml_row += "</url>\n"
    return xml_row

def detect_csv_type(first_row):
    """Detects the type of CSV based on headers or data."""
    headers = [h.strip().lower() for h in first_row]
    if "loc" in headers and "changefreq" in headers and "priority" in headers:
        return "full"
    elif "loc" in headers:
        return "loc_only"
    else:
        return "no_header"

def process_txt_file(txt_file):
    """Reads a TXT file and yields URL data."""
    with open(txt_file, 'r', encoding='utf-8-sig') as f:
        for row_number, line in enumerate(f, start=1):
            loc = line.strip()
            if not loc:
                print(f"WARNING: Empty line at row {row_number} skipped.")
                continue
            parsed = urlparse(loc)
            if not parsed.scheme or not parsed.netloc:
                print(f"ERROR: Invalid URL at row {row_number}: {loc}")
                continue
            yield loc, "daily", generate_priority(loc)

def deduplicate_urls(url_tuples):
    """Remove duplicate URLs while preserving order."""
    seen = set()
    deduped = []
    for loc, changefreq, priority in url_tuples:
        if loc not in seen:
            seen.add(loc)
            deduped.append((loc, changefreq, priority))
    return deduped

def convert_csv_to_xml(input_file, filename_input=None):
    """Convert CSV/TXT file to XML sitemap with dynamic column handling and deduplication."""
    if filename_input:
        xml_file_name = f"{filename_input}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"
    else:
        xml_file_name = f"xml_file_output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xml"
    file_ext = os.path.splitext(input_file)[1].lower()
    all_entries = []
    if file_ext == ".txt":
        all_entries.extend(process_txt_file(input_file))
    else:  # CSV
        with open(input_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
            sample = csvfile.readline().strip().split(",")
            csvfile.seek(0)
            csv_type = detect_csv_type(sample)
            if csv_type == "full":
                reader = csv.DictReader(csvfile)
            elif csv_type == "loc_only":
                reader = csv.DictReader(csvfile)
            else:
                reader = csv.reader(csvfile)
            for row_number, row in enumerate(reader, start=2):
                if csv_type == "full":
                    loc = row.get('loc', '').strip()
                    changefreq = row.get('changefreq', '').strip()
                    priority = row.get('priority', '').strip()
                elif csv_type == "loc_only":
                    loc = row.get('loc', '').strip()
                    changefreq = "daily"
                    priority = generate_priority(loc)
                else:
                    loc = row[0].strip() if row else ""
                    changefreq = "daily"
                    priority = generate_priority(loc)
                if not loc:
                    print(f"ERROR: Missing URL in row {row_number}")
                    continue
                parsed = urlparse(loc)
                if not parsed.scheme or not parsed.netloc:
                    print(f"ERROR: Invalid URL in row {row_number}: {loc}")
                    continue
                all_entries.append((loc, changefreq, priority))
    # deduplicate
    before_count = len(all_entries)
    all_entries = deduplicate_urls(all_entries)
    after_count = len(all_entries)
    removed_count = before_count - after_count
    # make XML
    with open(xml_file_name, 'w', encoding='utf-8') as xmlfile:
        xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xmlfile.write('<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for loc, changefreq, priority in all_entries:
            xmlfile.write(generate_xml_row(loc, changefreq, priority))
        xmlfile.write('</urlset>\n')
    print(f"Conversion completed successfully.\n"
          f"Data saved to {os.path.abspath(xml_file_name)}")
    if removed_count > 0:
        print(f"Note: {removed_count} duplicate URLs were removed.")

def main():
    parser = argparse.ArgumentParser(
        prog="Simple CSV/TXT to XML File Converter",
        description="Converts CSV/TXT to XML sitemap with dynamic column handling and deduplication.",
        epilog="Developed by JDT",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--input", help="Full path to the CSV or TXT file to convert.")
    parser.add_argument("--output", help="Base name for the output XML file (without extension).")
    args = parser.parse_args()
    # input file
    input_file = args.input
    if not input_file:
        print(menu_message)
        input_file = input("Enter the path to the CSV/TXT file: ").strip()
        while not validate_file_path(input_file):
            print("Invalid file path. Please enter a valid path.")
            input_file = input("Enter the path to the CSV/TXT file: ").strip()
    # output filename
    filename_input = args.output
    if not filename_input:
        filename_input = input("Enter the name for the output XML file (Press Enter for default): ").strip()
        if not filename_input:
            filename_input = None

    convert_csv_to_xml(input_file, filename_input)

if __name__ == "__main__":
    main()
