# xmllink transform - lower case

import xml.etree.ElementTree as ET

def transform_xml_to_lowercase(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find all <loc> elements and transform their text content to lowercase
    for loc_element in root.iter('loc'):
        loc_element.text = loc_element.text.lower()

    # Save the modified XML back to the file
    tree.write(xml_file_path)

if __name__ == "__main__":
    # Replace 'your_input.xml' with the actual XML file path
    input_xml_file = 'your_input.xml'
    
    try:
        transform_xml_to_lowercase(input_xml_file)
        print(f"Transformation successful. Check the modified content in {input_xml_file}")
    except Exception as e:
        print(f"Error: {e}")
