# Importing libraries
import re
import requests
from bs4 import BeautifulSoup

# Getting input for website from the user
url_input = input("Enter url: ")

# Check if the URL lacks the protocol scheme (http:// or https://)
if not url_input.startswith("http://") and not url_input.startswith("https://"):
    use_https = input("The input is missing a protocol scheme. Use HTTPS? Type 'Yes' or 'No': ").strip().lower()
    if use_https == "no":
        protocol = input("Please indicate the proper protocol to use or type 'None': ").strip()
        if protocol.lower() != 'none':
            url_input = protocol + "://" + url_input
    elif use_https != "yes":
        print("Invalid choice. Assuming HTTPS protocol.")
    else:
        url_input = "https://" + url_input

print("This is the website link that you entered:", url_input)

# Creating a unique set of links
all_links = set()

# Initialize a list with the starting URL
to_crawl = [url_input]

# Prompt the user for the desired crawl depth
crawl_depth = input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
if crawl_depth:
    crawl_depth = int(crawl_depth)
else:
    crawl_depth = float('inf')  # Set to infinity to crawl the entire site

# Define a function to check if a link is within the specified crawl depth
def within_crawl_depth(link_depth):
    return link_depth <= crawl_depth

# Define a dictionary to keep track of link depths
link_depths = {url_input: 0}

# Keep crawling as long as there are URLs to crawl within the specified depth
while to_crawl:
    current_url = to_crawl.pop(0)  # Get the next URL to crawl
    current_depth = link_depths[current_url]
    
    if current_depth <= crawl_depth:
        r = requests.get(current_url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        for link in soup.find_all("a", href=re.compile('/')):
            link = (link.get('href'))
            
            # For the removal of duplicate URLs, We will simply add a link to that set; this assures that it's distinct
            if link not in all_links:
                print(link)
                all_links.add(link)
                link_depths[link] = current_depth + 1
                
                # Add the new link to the list of URLs to crawl if it's within the specified depth
                if within_crawl_depth(current_depth + 1):
                    to_crawl.append(link)
