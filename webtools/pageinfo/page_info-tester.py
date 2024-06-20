import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# exceptions
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as _:
           print(f"\nError making request for: {repr(_)} - Exiting...\n")
        except ValueError as _:
            print(f"\nInvalid input: {repr(_)} - Exiting...\n")
        except KeyboardInterrupt as _:
            print(f"\nUser Interrupt: {repr(_)} - Exiting...\n")
        except FileNotFoundError as _:
            print(f"\nFile : {repr(_)} - Exiting...\n")
        except Exception as _:
            print(f"\nError: {repr(_)} - Exiting...\n")
    return wrapper

def get_user_input():
    while True:
        input_file_location = input("Enter the input CSV file location: ")
        if not validate_file_location(input_file_location):
            print("Invalid file location.")
            return
        output_filename = input("Enter the output filename (will save as CSV) or press Enter for default, 'page_url_info.csv': ").strip()
        if output_filename == "":
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_filename = f'page_url_info-{current_time}.csv'
        else:
            output_filename = f'{output_filename}.csv'
        return input_file_location, output_filename

def validate_file_location(file_location):
    return os.path.exists(file_location) and os.path.isfile(file_location)

def process_url_file(input_file_location, output_filename):
    with open(input_file_location, 'r', encoding='utf-8') as csvfile:
        urls = [row[0].strip('\ufeff') for row in csv.reader(csvfile)]
    headers = ['url', 'status_code', 'title', 'meta_description', 'canonical_link', 'h1']
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()  
        page_info = []
        for url in urls:
            data = get_page_info(url)
            writer.writerow(data)
            page_info.append(data)
            print(f"Saved: {url}")
    #return page_info

def get_page_info(url):
    response = requests.get(url, timeout=20)
    # response.raise_for_status()
    status_code = response.status_code
    if status_code == 404:
        return {
            'url': url,
            'status_code': status_code,
            'title': "",
            'meta_description': "",
            'canonical_link': "",
            'h1': ""
        }
    page_markup = response.content
    soup = BeautifulSoup(page_markup, "html.parser")
    title = soup.title.string.strip() if soup.title else "No title"
    canonical_tag = soup.head.find("link", rel="canonical", href=True)
    canonical_link = canonical_tag["href"].strip() if canonical_tag else "No canonical present"
    meta_tag = soup.head.find("meta", attrs={"name": "description"})
    meta_desc = meta_tag["content"].strip() if meta_tag and "content" in meta_tag.attrs else "No meta description"
    h1_tag = soup.find('h1').text.strip() if soup.find('h1') else "No h1 tag found"
    # return url, status_code, title, meta_desc, canonical_link, h1_tag
    return {
        'url': url,
        'status_code': status_code,
        'title': title,
        'meta_description': meta_desc,
        'canonical_link': canonical_link,
        'h1': h1_tag
    }

# def save_to_csv(data, filename):
#     headers = ['url', 'status_code', 'title', 'meta_description', 'canonical_link', 'h1']
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=headers)
#         writer.writeheader()
#         writer.writerows(data)

@handle_exceptions
def main():
    input_file_location, output_filename = get_user_input()
    process_url_file(input_file_location, output_filename)
    # save_to_csv(page_info, output_filename)
    print(f"Data saved to {os.path.abspath(output_filename)}")

if __name__ == '__main__':
    main()