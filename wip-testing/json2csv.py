'''json2csv.py
This script transforms JSON data into a CSV file. Multiple levels of nesting are supported. 
Any data types that are not JSON objects or arrays are converted to strings.
Nested dictionaries and lists are converted to strings and concatenated with a comma.

Usage: json2csv.py <input_file> <output_file>
Example: json2csv.py input.json output.csv

Not working, further testing needed

'''

# imports
import json
import csv
import sys

# main function
def main():
    if len(sys.argv) < 3:
        print("Usage: json2csv.py <input_file> <output_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as input_file:
        data = json.load(input_file)

    output_data = []
    for row in data:
        output_row = []
        for key, value in row.items():
            if isinstance(value, (dict, list)):
                output_row.append(json.dumps(value))
            elif isinstance(value, str):
                output_row.append(value)
            elif isinstance(value, bool):
                output_row.append(str(value).lower())
            elif isinstance(value, (int, float)):
                output_row.append(str(value))
            elif value is None:
                output_row.append('')
            else:
                output_row.append(str(value))
        output_data.append(output_row)

    with open(sys.argv[2], 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output_data)

    print(f"Data written to {sys.argv[2]}")

# call main function
if __name__ == '__main__':
    main()