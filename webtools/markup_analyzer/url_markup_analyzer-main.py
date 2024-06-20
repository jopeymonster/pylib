# url_markup_analyzer.py
# URL crawl markup tags and output to console or file (csv/json, custom name option or default)

# dev:
# - multiple {user_url} targets as option
# - option to ingest/input an .html file instead of crawling a page = needs fixing (local var access)

import os
import re
import requests
from bs4 import BeautifulSoup
import json

def process_input_url(url):
    # Handling input URLs without a protocol scheme
    if not re.match(r"^https?://", url):
        use_https = input("The input is missing a protocol scheme. Use HTTPS? (Y)es or (N)o?: ").strip().lower()
        if use_https in ['no', 'n']:
            protocol = input("Please indicate the proper protocol to use (http/https) or type 'None': ").strip()
            if protocol.lower() != 'none':
                url = f"{protocol}://{url}"
            else:
                print("Invalid input. Assuming HTTPS protocol.")
                url = f"https://{url}"
        elif use_https in ['yes', 'y']:
            url = f"https://{url}"
        else:
            print("Invalid choice. Assuming HTTPS protocol.")
            url = f"https://{url}"
    print("Processed URL:", url)
    return url

def validate_url(url):
    # Validate if the URL is reachable
    response = requests.get(url)
    if response.status_code != 200:
        print(f"This URL is not valid ({response.status_code}), please provide a new URL")
        return None
    else:
        print("URL is valid and will be analyzed.")
        return url

def output_data_from_url(validated_url, user_param):
    try:
        user_choice = input("Would you like to save the analyzed data to a file? (Y)es or (N)o? ").strip().lower()
        if user_choice in ['yes', 'y']:
            file_name = input(f"Enter desired file name now or leave empty for default ({validated_url}-markup-analyzer): ").strip()
            if not file_name:
                file_name = f"{validated_url}-markup-analyzer"
            else:
                file_name = file_name
            output_format = input("Choose saved file format:\n"
                                  "1. CSV\n"
                                  "2. JSON\n"
                                  "Enter option number: ")
            while output_format not in ['1', '2']:
                print("Invalid option. Please select '1' for CSV or '2' for JSON.")
                output_format = input("Choose saved file format:\n"
                                      "1. CSV\n"
                                      "2. JSON\n"
                                      "Enter option number: ")
            output_format = 'csv' if output_format == '1' else 'json'
            if not os.path.exists(f"{file_name}.{output_format}"):
                with open(f"{file_name}.{output_format}", 'w', encoding='utf-8') as file:
                    if output_format == 'csv':
                        file.write('Tag Type,Attributes\n')
                        tag_count = 0
                        if validated_url.startswith('http'):
                            response = requests.get(validated_url)
                            soup = BeautifulSoup(response.content, 'html.parser')
                        else:
                            with open(validated_url, 'r', encoding='utf-8') as html_file:
                                soup = BeautifulSoup(html_file, 'html.parser')
                        if user_param.strip():
                            tags = soup.find_all(attrs={'class': user_param})
                        else:
                            tags = soup.find_all()
                        for tag in tags:
                            tag_count += 1
                            if tag.name == "a":
                                tag_name = "hyperlink"
                            elif tag.name == "li":
                                tag.name = "list"
                            elif tag.name == "p":
                                tag.name = "paragraph"
                            elif tag.name == "script":
                                tag.name = "javascript"
                            else:
                                tag_name = tag.name
                            file.write(f"{tag_name},{tag.attrs}\n")
                        input(f"Total number of tags counted: {tag_count}\nPress ENTER to continue.\n")
                    else:
                        data = []
                        tag_count = 0
                        if validated_url.startswith('http'):
                            response = requests.get(validated_url)
                            soup = BeautifulSoup(response.content, 'html.parser')
                        else:
                            with open(validated_url, 'r', encoding='utf-8') as html_file:
                                soup = BeautifulSoup(html_file, 'html.parser')
                        if user_param.strip():
                            tags = soup.find_all(attrs={'class': user_param})
                        else:
                            tags = soup.find_all()
                        for tag in tags:
                            tag_count += 1
                            if tag.name == "a":
                                tag_name = "hyperlink"
                            elif tag.name == "li":
                                tag.name = "list"
                            elif tag.name == "p":
                                tag.name = "paragraph"
                            elif tag.name == "script":
                                tag.name = "javascript"
                            else:
                                tag_name = tag.name
                            data.append({f"Tag": tag_count, "Tag Type": tag_name, "Attributes": tag.attrs})
                        json.dump(data, file, indent=4)
                        input(f"Total number of tags counted: {tag_count}\nPress ENTER to continue.\n")
            else:
                print(f"File '{file_name}.{output_format}' already exists. Please choose a different name.")
        elif user_choice in ['no', 'n']:
            print("Output to console. No file will be created.")
            if not user_param or not user_param.strip():
                input(f"This tool will analyze the webpage: {validated_url}\nSearching all tags and analyzing all attributes.\nPress ENTER to proceed.\n")
            else:
                input(f"This tool will analyze the webpage: {validated_url}\nSearching for any class or ID containing: {user_param}.\nPress ENTER to proceed.\n")
            response = requests.get(validated_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            tags = soup.find_all(attrs={'class': user_param})
            for i, tag in enumerate(tags, 1):
                if tag.name == "a":
                    tag_name = "hyperlink"
                elif tag.name == "li":
                    tag.name = "list"
                elif tag.name == "p":
                    tag.name = "paragraph"
                elif tag.name == "script":
                    tag.name = "javascript"
                else:
                    tag_name = tag.name
                print(f"{i}. Tag Type: {tag_name}")
                for j, (attr, value) in enumerate(tag.attrs.items(), 1):
                    value_str = ' '.join(value) if isinstance(value, list) else value
                    attr_str = f"{j}. {attr}:".ljust(1)
                    print(f"   {attr_str} {value_str}")
            input(f"Total number of tags counted: {i}\nPress ENTER to continue.\n")
        else:
            print("Invalid option.")
    except Exception as ex:
        print(f"An error occurred: {ex}")

# WIP for csv output from input file - formatting issues
def output_data_from_file(html_file, user_param):
    try:
        user_choice = input("Would you like to save the analyzed data to a file? (Y)es or (N)o? ").strip().lower()
        if user_choice in ['yes', 'y']:
            file_name = input(f"Enter desired file name now or leave empty for default ({html_file}-markup-analyzer): ").strip()
            if not file_name:
                file_name = f"{html_file}-markup-analyzer"
            else:
                file_name = file_name
            output_format = input("Choose saved file format:\n"
                                  "1. CSV (WIP for file input analysis)\n"
                                  "2. JSON\n"
                                  "Enter option number: ")
            while output_format not in ['1', '2']:
                print("Invalid option. Please select '1' for CSV or '2' for JSON.")
                output_format = input("Choose saved file format:\n"
                                      "1. CSV (WIP for file input analysis)\n"
                                      "2. JSON\n"
                                      "Enter option number: ")
            output_format = 'csv' if output_format == '1' else 'json'
            if not os.path.exists(f"{file_name}.{output_format}"):
                with open(html_file, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    with open(f"{file_name}.{output_format}", 'w', encoding='utf-8') as output_file:
                        if output_format == 'csv':
                            output_file.write('Tag Type,Attributes\n')
                            tag_count = 0
                            if user_param.strip():
                                tags = soup.find_all(attrs={'class': user_param})
                            else:
                                tags = soup.find_all()
                            for tag in tags:
                                tag_count += 1
                                if tag.name == "a":
                                    tag_name = "hyperlink"
                                elif tag.name == "li":
                                    tag_name = "list"
                                elif tag.name == "p":
                                    tag_name = "paragraph"
                                elif tag.name == "script":
                                    tag_name = "javascript"
                                else:
                                    tag_name = tag.name
                                attributes = ', '.join([f"{attr}=\"{value}\"" for attr, value in tag.attrs.items()])
                                output_file.write(f"{tag_name},{attributes}\n")
                            input(f"Total number of tags counted: {tag_count}\nPress ENTER to continue.\n")
                        else:
                            data = []
                            tag_count = 0
                            if user_param.strip():
                                tags = soup.find_all(attrs={'class': user_param})
                            else:
                                tags = soup.find_all()
                            for tag in tags:
                                tag_count += 1
                                tag_name = tag.name if tag.name not in ["a", "li", "p", "script"] else \
                                    "hyperlink" if tag.name == "a" else \
                                    "list" if tag.name == "li" else \
                                    "paragraph" if tag.name == "p" else \
                                    "javascript" if tag.name == "script" else None
                                data.append({f"Tag": tag_count, "Tag Type": tag_name, "Attributes": tag.attrs})
                            json.dump(data, output_file, indent=4)
                            input(f"Total number of tags counted: {tag_count}\nPress ENTER to continue.\n")
                            pass
            else:
                print(f"File '{file_name}.{output_format}' already exists. Please choose a different name.")
        elif user_choice in ['no', 'n']:
            print("Output to console. No save file will be created.")
            if not user_param or not user_param.strip():
                input(f"This tool will analyze the file: {html_file}\nSearching all tags and analyzing all attributes.\nPress ENTER to proceed.\n")
            else:
                input(f"This tool will analyze the file: {html_file}\nSearching for any class or ID containing: {user_param}.\nPress ENTER to proceed.\n")
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                base_url = soup.base['href'] if soup.base else None
                tags = soup.find_all(attrs={'class': user_param})
                for i, tag in enumerate(tags, 1):
                    tag_name = tag.name if tag.name not in ["a", "li", "p", "script"] else \
                            "hyperlink" if tag.name == "a" else \
                            "list" if tag.name == "li" else \
                            "paragraph" if tag.name == "p" else \
                            "javascript" if tag.name == "script" else None
                    print(f"{i}. Tag Type: {tag_name}")
                    for j, (attr, value) in enumerate(tag.attrs.items(), 1):
                        if attr == 'href':
                            base_url = soup.base['href'] if soup.base else None
                            if base_url and not value.startswith('http'):
                                value = base_url.rstrip('/') + '/' + value.lstrip('/')
                            value = value.strip()
                        if isinstance(value, list):
                            value = ' '.join(value)
                        print(f"   {j}. {attr}: {value}")
                input(f"Total number of tags counted: {i}\nPress ENTER to continue.\n")
            pass        
        else:
            print("Invalid option.")
    except Exception as ex:
        print(f"An error occurred: {ex}")

# Main logic
print("URL Markup Analyzer, by JDT")
while True:
    user_option = input("Choose an option:\n"
                        "1. Analyze a webpage by URL\n"
                        "2. Input an HTML file for analysis\n"
                        "3. Exit\n"
                        "Enter option number: ")
    if user_option == '1':
        user_url = input("Enter the URL to analyze: ")
        proper_url = process_input_url(user_url)
        validated_url = validate_url(proper_url)
        if validated_url:
            user_param = input("Provide a parameter to search for or leave blank to analyze all tags: ")
            output_data_from_url(validated_url, user_param)
    elif user_option == '2':
        html_file = input("Enter the path to the HTML file: ")
        if not os.path.exists(html_file):
            print("File not found.")
        else:
            user_param = input("Provide a parameter to search for or leave blank to analyze all tags: ")
            output_data_from_file(html_file, user_param)
    elif user_option == '3':
        break
    else:
        print("Invalid option. Please select 1, 2, or 3.")