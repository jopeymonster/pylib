#JDT.082523

import json
import os

def remove_object_from_json(json_data, target_object):
    if isinstance(json_data, dict):
        for key, value in list(json_data.items()):
            if value == target_object:
                json_data.pop(key)
                print("Removed empty object")
            elif isinstance(value, (dict, list)):
                remove_object_from_json(value, target_object)
    elif isinstance(json_data, list):
        for idx, item in enumerate(json_data):
            if item == target_object:
                json_data.pop(idx)
                print("Removed empty object")
            elif isinstance(item, (dict, list)):
                remove_object_from_json(item, target_object)

def main():
    input_file_path = input("Enter the file location of the input JSON file: ")

    if not os.path.exists(input_file_path):
        print("Input file does not exist.")
        return

    output_file_path = os.path.join(
        os.path.dirname(input_file_path),
        os.path.basename(input_file_path).replace(".json", "-fixed.json")
    )
    
    target_object = {
        "type": "",
        "hidden": False
    }

    with open(input_file_path, "r") as input_file:
        json_data = json.load(input_file)

    remove_object_from_json(json_data, target_object)

    with open(output_file_path, "w") as output_file:
        json.dump(json_data, output_file, indent=4)
    
    print("Script completed. Check the output file for results.")

if __name__ == "__main__":
    main()
