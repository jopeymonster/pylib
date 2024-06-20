import json

def find_key_value(obj, keys, path='', results=None):
    if results is None:
        results = []

    # Define a recursive function to traverse the JSON structure
    def search_json(value, current_path=''):
        if isinstance(value, dict):
            for key, val in value.items():
                new_path = f"{current_path}.{key}" if current_path else key
                search_json(val, new_path)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                new_path = f"{current_path}[{i}]"
                search_json(item, new_path)
        elif isinstance(value, (str, int, float, bool, type(None))):
            if any(current_path.endswith(f".{k}") for k in keys):
                results.append((current_path, value))

    # Search for specified keys in the JSON structure
    search_json(obj, path)

    return results

if __name__ == "__main__":
    # Prompt user for file location
    file_path = input("Enter the file location of the JSON file: ")

    # Load JSON data from file
    with open(file_path) as json_file:
        data = json.load(json_file)

    # Prompt user for keys
    user_keys = input("Enter keys separated by commas: ").split(',')

    # Execute the script
    results = find_key_value(data, user_keys)

    # Print results
    for key, value in results:
        print(f"Key: {key}, Value: {value}")
