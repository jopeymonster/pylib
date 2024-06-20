"""flattenjson.py
This code snippet defines functions for flattening JSON data, 
getting user input for a JSON file path, and outputting the flattened data either to the console or a file. 
The main function orchestrates the process by getting data from the user, 
flattening it, and then outputting the flattened data based on user choice.

NOT WORKING, FURTHER TESTING NEEDED
"""
import json
import sys
import os
# import tabulate

def get_data():
    data = input("Enter path to JSON file: ")
    return data

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def get_filename():
    filename = input("Please enter the filename: ")
    return filename + '.json'

def output_data(data: dict) -> None:
    if not data:
        print("No data to output")
        return
    print("Would you like to output the data to:\n1. Console\n2. File")
    output_choice = input("Please enter 1 or 2: ")
    if output_choice == "1":
        print(json.dumps(data, indent=2))
    elif output_choice == "2":
        filename = get_filename()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data written to {os.path.abspath(filename)}")

def main():
    data = get_data()
    flattened = flatten_json(data)
    output_data(flattened)

if (__name__ == '__main__'):
    main()