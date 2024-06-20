# Link crawler - status checker, crawl depth options / outputs only errors

# Importing libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Get the HTTP status code of a URL
def get_status_code(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Returns HTTPError for bad responses (4xx and 5xx)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return str(e)
""""
    Args:
    url (str): The URL to check.
Returns:
    int: The HTTP status code.
    If the request fails, returns the error message as a string.
"""

# Function to prompt user for protocol
def prompt_protocol():
    use_https = input("The input is missing a protocol scheme. Use HTTPS? Type Y, Yes, N or No: ").strip().lower()
    if use_https in ['no', 'n']:
        protocol = input("Please indicate the proper protocol to use (http/https) or type 'None': ").strip()
        if protocol.lower() != 'none':
            return protocol
        else:
            print("Invalid input. Assuming HTTPS protocol.")
            return "https"
    elif use_https in ['yes', 'y']:
        return "https"
    else:
        print("Invalid choice. Assuming HTTPS protocol.")
        return "https"

def get_user_input_url():
    while True:
        url_input = input("Enter url: ")
        if not url_input.startswith("http://") and not url_input.startswith("https://"):
            protocol = prompt_protocol()
            url_input = f"{protocol}://{url_input}"
        print("This is the website link that you entered: ", url_input)
        return url_input
            
# Get URL input to crawl
url_input = get_user_input_url()

# Prompt user for desired crawl depth
crawl_depth = input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
if crawl_depth: # Convert to int and check if valid
    crawl_depth = int(crawl_depth)
    if crawl_depth > 0:
        print(f"Executing crawl with a depth of {crawl_depth}. ")
    else: # Handle invalids
        print("ERROR: Crawl depth must be an number greater than 0, defaulting to crawl depth of 1")
        crawl_depth = 1
else:
    print("Executing full site crawl.")
    crawl_depth = float('inf')  # Set to infinity to crawl the entire site

# Define a function to check if a link is within the specified crawl depth
def within_crawl_depth(link_depth):
    return link_depth <= crawl_depth

# Define a dictionary to keep track of link depths
link_depths = {url_input: 0}
all_links = set()

# Initialize a list with the starting URL
to_crawl = [url_input]

# Add these lines before the while loop to count URLs and errors
counted_urls = 0
total_errors = 0

# Keep crawling as long as there are URLs to crawl within the specified depth
while to_crawl:
    current_url = to_crawl.pop(0)  # Get the next URL to crawl
    current_depth = link_depths[current_url]
    
    if current_depth <= crawl_depth:
        status_code = get_status_code(current_url) # Get link status code
        
        # Check if status_code is a string that can be converted to an integer
        if isinstance(status_code, str):
            if status_code.isdigit():
                status_code = int(status_code)
            else:
                # Handle the case where status_code is not a valid integer
                print(f"Error, Invalid Status Code: {status_code} | URL: {current_url}")
                continue

        if status_code >= 400:  # Check if it's a client error (4xx) or server error (5xx)
            print(f"Error, Client or Server: {status_code} | URL: {current_url}")
            total_errors += 1
            counted_urls += 1 # Increment the counter only for error URLs
        else:
            counted_urls += 1  # Increment the counter only for successful URLs
        
            if counted_urls % 10 == 0: # Calculate total crawled per 10 and print status
                print(f"Analysis in progress... counted {counted_urls} URLs so far.")

            if current_depth == crawl_depth:
                continue  # Skip further processing for links at the maximum depth
            
            r = requests.get(current_url)
            soup = BeautifulSoup(r.content, "html.parser")
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
    
    # Print progress message every 10 URLs checked
    if counted_urls % 10 == 0:
        print(f"Analysis in progress... counted {counted_urls} URLs so far.")

# Print the summary once the analysis is complete
print(f"Analyzed {counted_urls} URLs. Total errors: {total_errors}")