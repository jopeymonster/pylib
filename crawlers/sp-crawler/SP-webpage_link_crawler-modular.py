import sys
import os
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from _pack.crawler import Crawler
from _pack import sp_const

# Define global variables
url_input = ""
crawl_depth = 0
file_name = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
}

# prop list
def prop_list():
    for designation, url in sp_const.PROPS.items():
        print(f'{designation}: {url}')

# get user input URL
def get_crawl_seed():
    prop_list()
    while True:
        init_prompt = input("Enter property initials as above or input ANY URL: ").upper()
        if len(init_prompt) == 2 and init_prompt in sp_const.PROPS:
            print(f"The winner is...{sp_const.PROPS[init_prompt]}")
            return sp_const.PROPS[init_prompt]
        elif Crawler.is_valid_url(init_prompt):
            print(f"The winner is...{init_prompt}")
            return init_prompt
        else:
            print("Invalid input. Please enter a 2-letter character designation or a valid URL.")

# get file name from user
def get_file_name():
    file_name = input("Enter desired file name now or leave empty for default (url-crawl-output.csv): ").strip()
    if not file_name:
        file_name = "url-crawl-output.csv"
    else:
        file_name = file_name + ".csv"
    # initialize a new file with headers if none
    if not Crawler.file_exists(file_name):
        Crawler.initialize_file(file_name)
    return file_name

# get crawl depth from user
def get_crawl_depth():
    # Prompt the user for the desired crawl depth
    crawl_depth_input = input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
    if crawl_depth_input:
        return int(crawl_depth_input)
    else:
        return float('inf')  # Set to infinity to crawl the entire site
    
def save_to_file(file_name, data):
    try:
        file_exists = os.path.exists(file_name)
        with open(file_name, 'a', newline='', encoding='utf-8') as file:
            if not file_exists:
                file.write('URL,StatusCode,Title,Meta Description,Canonical Link\n')
            for row in data:
                # double quotes to handle commas
                row = ['"{}"'.format(value) for value in row]
                file.write(','.join(row) + '\n')
    except Exception as e:
        print(f"Error saving to file: {e}")

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
        url_input = get_crawl_seed()
    else:
        url_input = sp_const.PROPS.get(url_input.upper())

    # check url validity
    valid_url = Crawler(url_input, crawl_depth, headers)
    if not valid_url.is_valid_url(url_input):
        print ("Invalid URL. Please Enter a valid URL.")
        sys.exit(1)

    crawl_depth = int(args.crawl_depth) if args.crawl_depth else get_crawl_depth()
    file_name = args.file_name if args.file_name else get_file_name()

    # Create a Crawler instance
    crawler = Crawler(url_input, crawl_depth, file_name)

    # Crawl
    crawler.crawl()

    # save output data to file
    save_to_file(file_name, crawler.output_data)
    print(f"Identified {len(crawler.crawled_urls)} links | Saved output to {file_name}")

if __name__ == '__main__':
    main()
