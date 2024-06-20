# Link crawler - status checker, crawl depth options / csv output all links data: url, status, page title, meta description and canonical link
# option to output to console, save to file w/custom name or save to file with default

# Importing libraries
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to make a request and parse the response
def get_response_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        return str(e)

# Function to extract information (e.g., title, description, canonical link) from HTML content
def extract_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.title.string.strip() if soup.title else "No title"
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical_link = canonical_tag["href"].strip() if canonical_tag else "No canonical present"
    return title, canonical_link

# Function to get meta description, handled separate due to possible empty output
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

# Function to check the status code of a URL
def get_status_code(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return str(e)

# Function to validate a URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to get user input URL
def get_user_input_url():
    while True:
        url_input = input("Enter URL: ")
        if not is_valid_url(url_input):
            print("Invalid URL. Please enter a valid URL.")
            continue
        return url_input
            
# Getting input for website from the user
url_input = get_user_input_url()

# Prompt the user for the desired crawl depth
crawl_depth = input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
if crawl_depth:
    crawl_depth = int(crawl_depth)
else:
    crawl_depth = float('inf')  # Set to infinity to crawl the entire site

# Getting input for file name from the user
file_name = input("Enter desired file name now or leave empty for default (url-crawl-output.csv): ").strip()
if not file_name:
    file_name = "url-crawl-output.csv"
else:
    file_name = file_name + ".csv"

# Check if the file exists or create a new file with headers
if not os.path.exists(file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        file.write('URL,Status Code,Title,Meta Description,Canonical Link\n')

# Function to save output to a file
def save_to_file(data):
    try:
        with open(file_name, 'a', newline='', encoding='utf-8') as file:
            for row in data:
                # Enclose values in double quotes to handle commas
                row = ['"{}"'.format(value) for value in row]
                file.write(','.join(row) + '\n')
        # print(f"Saved output to {file_name}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Define a function to check if a link is within the specified crawl depth
def within_crawl_depth(link_depth):
    return link_depth <= crawl_depth

# Define a dictionary to keep track of link depths
link_depths = {url_input: 0}
all_links = set()

# Initialize a list with the starting URL
to_crawl = [url_input]

# Initialize the output_data list outside the loop
output_data = []

# count URLs and errors
counted_urls = 0
total_errors = 0

# Keep crawling as long as there are URLs to crawl within the specified depth
while to_crawl:
    current_url = to_crawl.pop(0)  # Get the next URL to crawl
    current_depth = link_depths[current_url]

    if current_depth <= crawl_depth:
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
            counted_urls += 1 # Increment the counter only for error URLs
        else:
            counted_urls += 1  # Increment the counter only for successful URLs
            print(f"{current_url} - saved to file")
            if counted_urls % 50 == 0: # Calculate total crawled per 50 and print status
                print(f"Analysis in progress... counted {counted_urls} URLs so far.")

        # Append the data to the output_data list
        output_data.append([
            current_url, f"{status_code}", title, description, canonical_link
        ])

        if current_depth == crawl_depth:
            continue  # Skip further processing for links at the maximum depth        

        if current_depth == crawl_depth:
            continue  # Skip further processing for links at the maximum depth

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

                # For the removal of duplicate URLs, We will simply add a link to that set; this assures that it's distinct
                if absolute_link not in all_links:
                    all_links.add(absolute_link)
                    link_depths[absolute_link] = current_depth + 1

                    # Add the new link to the list of URLs to crawl if it's within the specified depth
                    if within_crawl_depth(current_depth + 1):
                        to_crawl.append(absolute_link)

save_to_file(output_data)