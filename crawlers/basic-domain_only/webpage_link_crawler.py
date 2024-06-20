# imports
import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from _pack import _const

# Define global variables
url_input = ""
crawl_depth = 0
file_name = ""

# saved url list
def saved_url_list():
    for designation, url in _const.SAVED_URLS.items():
        print(f'{designation}: {url}')

# make a request and parse the response
def get_response_data(url):
    try:
        response = requests.get(url, headers={"User-Agent": "-[.:JoesSpiderFarm-wblc-v1:.]-"})
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        return str(e)

# extract information (e.g., title, description, canonical link) from HTML content
def extract_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.title.string.strip() if soup.title else "No title"
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical_link = canonical_tag["href"].strip() if canonical_tag else "No canonical present"
    return title, canonical_link

# get meta description, handled separately due to possible empty output
def get_meta_description(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and "content" in meta_tag.attrs:
            return meta_tag["content"].strip()
        return "No meta description"
    except requests.exceptions.RequestException as e:
        return str(e)

# check the status code of a URL
def get_status_code(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return str(e)

# validate a URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Define a function to check if a link is within the specified crawl depth
def within_crawl_depth(link_depth, crawl_depth):
    return link_depth <= crawl_depth

# get user input URL
def get_user_input():
    saved_url_list()
    user_input = ""
    while True:
        init_prompt = input("Enter URL designation initials as above or input ANY URL: ").upper()
        if len(init_prompt) > 2:
            if not is_valid_url(init_prompt):
                print("Invalid URL. Please enter a valid URL.")
            else:
                print(f"The winner is...{init_prompt}")
                user_input = init_prompt
                break
        else:
            if init_prompt in _const.SAVED_URLS:
                print(f"The winner is...{_const.SAVED_URLS[init_prompt]}")
                user_input = _const.SAVED_URLS[init_prompt]
                break
            else:
                print("Invalid property designation.")
    return user_input

# get file name from user
def get_file_name():
    file_name = input("Enter desired file name now or leave empty for default (url-crawl-output.csv): ").strip()
    if not file_name:
        file_name = "url-crawl-output.csv"
    else:
        file_name = file_name + ".csv"
    # initalize a new file with headers if none
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            file.write('URL,Status Code,Title,Meta Description,Canonical Link\n')
    return file_name

# save output to a file
def save_to_file(file_name, data):
    try:
        with open(file_name, 'a', newline='', encoding='utf-8') as file:
            for row in data:
                # Enclose values in double quotes to handle commas
                row = ['"{}"'.format(value) for value in row]
                file.write(','.join(row) + '\n')
        # print(f"Saved output to {file_name}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def get_crawl_depth():
    # Prompt the user for the desired crawl depth
    crawl_depth_input = input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
    if crawl_depth_input:
        return int(crawl_depth_input)
    else:
        return float('inf')  # Set to infinity to crawl the entire site

# main
def main():
    global url_input, crawl_depth, file_name

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Link crawler - status checker.')
    parser.add_argument('--i', '--initials', dest='initials', help='Property initials for URL input')
    parser.add_argument('--u', '--url', dest='url', help='Direct URL input')
    parser.add_argument('--c', '--crawl_depth', dest='crawl_depth', help='Crawl depth as an integer')
    parser.add_argument('--f', '--file_name', dest='file_name', help='File name for output')

    # Parse command line arguments
    args = parser.parse_args()

    # Use CLI arguments if provided
    url_input = args.url if args.url else args.initials
    if not url_input:
        url_input = get_user_input()
    else:
        url_input = _const.SAVED_URLS.get(url_input.upper())
    # Check if the provided URL is valid
    if not is_valid_url(url_input):
        print("Invalid URL. Please enter a valid URL.")
        sys.exit(1)

    crawl_depth = int(args.crawl_depth) if args.crawl_depth else get_crawl_depth()
    file_name = args.file_name if args.file_name else get_file_name()

    # Initialize a list with the starting URL and its depth
    to_crawl = [(url_input, 0)]

    # Initialize the output_data list outside the loop
    output_data = []

    # prompt for crawl depth and file name
    if crawl_depth is None:
        crawl_depth = get_crawl_depth()
    if not file_name:
        file_name = get_file_name()

    # A set to keep track of crawled URLs
    crawled_urls = set()

    # count URLs and errors
    counted_urls = 0
    total_errors = 0

    # Keep crawling as long as there are URLs to crawl within the specified depth
    while to_crawl:
        current_url, current_depth = to_crawl.pop(0)  # Get the next URL and its depth to crawl

        if current_depth <= crawl_depth and current_url not in crawled_urls:
            # Analyze URL
            html_content = get_response_data(current_url)
            status_code = get_status_code(current_url)
            title, canonical_link = extract_info(html_content)
            description = get_meta_description(current_url)

            # Skip processing if the URL is not valid
            if not is_valid_url(current_url):
                print(f"Invalid URL: {current_url}")
                continue

            if status_code >= 400:  # Check if it's a client error (4xx) or server error (5xx)
                print(f"Error, Client or Server: {status_code} | URL: {current_url}")
                total_errors += 1
            else:
                counted_urls += 1  # Increment the counter only for successful URLs
                print(f"{current_url} - saved to file")
                if counted_urls % 50 == 0:  # Calculate total crawled per 50 and print status
                    print(f"Analysis in progress... counted {counted_urls} URLs so far.")

            # Append the data to the output_data list
            output_data.append([
                current_url, f"{status_code}", title, description, canonical_link
            ])

            crawled_urls.add(current_url)  # Mark the URL as crawled

            soup = BeautifulSoup(html_content, "html.parser")
            for link in soup.find_all("a", href=True):
                link = link.get('href')

                # Skip if the link starts with "tel:" or "#"
                if "#" in link or link.startswith("tel:"):
                    continue

                # Check if the link ends with .html, .htm, or has no extension (assuming it's an HTML link)
                if link and (link.endswith(".html") or link.endswith(".htm") or not '.' in link):
                    # Resolve relative URLs to absolute URLs
                    absolute_link = urljoin(current_url, link)

                    # is link within the specified depth and belongs to the same domain
                    if within_crawl_depth(current_depth + 1, crawl_depth) and urlparse(absolute_link).netloc == urlparse(url_input).netloc:
                        # Add link to the list
                        to_crawl.append((absolute_link, current_depth + 1))

    save_to_file(file_name, output_data)
    print(f"Found {counted_urls} | Saved output to {file_name}")

# Run the main function if the script is executed
if __name__ == '__main__':
    main()
