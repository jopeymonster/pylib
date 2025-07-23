# imports
import sys
import os
import time
import re
from datetime import datetime
import requests
import argparse
import importlib.util
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Doctype
from requests.exceptions import RequestException
import helpers

# config file loading
def load_const_module(const_file=None):
    """Dynamically loads a constants.py file as a module."""
    if const_file is None:
        const_file = os.path.join(os.path.dirname(__file__), "core", "default_constants.py")
    if not os.path.exists(const_file):
        print(f"Constants file not found: {const_file}\n"
              "Please refer to the documentation for the proper setup.")
        sys.exit("Exiting due to missing constants file.")
    print(f"Using constants file: {const_file}")
    spec = importlib.util.spec_from_file_location("default_constants", const_file)
    const_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(const_module)
    return const_module

# validate URL
def is_valid_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc])

def get_crawl_depth():
    while True:
        crawl_depth_input = helpers.custom_input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
        if crawl_depth_input.strip().isdigit():
            return int(crawl_depth_input)
        elif not crawl_depth_input.strip():
            return float('inf')
        else:
            print("Invalid input. Please enter a valid integer or leave it blank.")

def get_targets(init_prompt, url, const):
    if init_prompt == 'XX':
        regex_pattern = r'(www\.)([\w-]+)(\.com|\.com\.au|\.eu)?'
        match = re.search(regex_pattern, url, re.IGNORECASE)
        if match:
            domain = match.group(2)
            for key, value in const.PROPS.items():
                if domain in value:
                    init_prompt = key
                    break
            else:
                print("Invalid URL input!")
                return "", "", ""
        else:
            print("Invalid URL input!")
            return "", "", ""
    while True:
        print("Select link target scope:\n"
              "1. NAV - only left menu links\n"
              "2. CONTENT - main content page links (excludes left nav, top and bottom header links)")
        tag_choice = helpers.custom_input("1 or 2: ")
        if tag_choice in {'1', '2'}:
            break
        else:
            print("Invalid input, please select 1 or 2")
    return handle_tag_choice(tag_choice, init_prompt, const)

def handle_tag_choice(tag_choice, init_prompt, const):
    if tag_choice == '1':
        target_tag = const.NAVTAGS.get(init_prompt, "")
        target_id = const.NAVIDS.get(init_prompt, "")
        target_class = const.NAVCLASSES.get(init_prompt, "")
    elif tag_choice =='2':
        target_tag = const.CONT_TAGS.get(init_prompt, "")
        target_id = const.CONT_IDS.get(init_prompt, "")
        target_class = const.CONT_CLASSES.get(init_prompt, "")
    return target_tag, target_id, target_class

def get_page_details(soup):
    title = soup.title.string.strip() if soup.title and soup.title.string is not None else "No title"
    canonical_tag = soup.head.find("link", rel="canonical")
    canonical_link = canonical_tag["href"].strip() if canonical_tag and canonical_tag.get("href") is not None else "No canonical present"
    meta_tag = soup.head.find("meta", attrs={"name": "description"})
    meta_desc = meta_tag["content"].strip() if meta_tag and "content" in meta_tag.attrs and meta_tag.get("content") is not None else "No meta description"
    return title, meta_desc, canonical_link

def get_page_info(url, headers, target_tag, target_id, target_class):
    try:
        response = requests.get(url, headers=headers, timeout=20)
        status_code = response.status_code
        if status_code in [404, 406]:
            return status_code, "", "", "", []
        page_markup = response.content
        soup = BeautifulSoup(page_markup, "html.parser")
        # check for doctype declaration
        doctype_pattern = re.compile(br"^\s*(<!--.*?-->\s*)*<!DOCTYPE html>", re.IGNORECASE | re.DOTALL)
        has_doctype = bool(doctype_pattern.match(page_markup))
        if not has_doctype:
            print(f"DTD missing: {url}")
            return status_code, "", "", "", []
        head_tag = soup.find("head")
        if head_tag is None:
            print(f"<head> tag not found: {url}")
        title, meta_desc, canonical_link = get_page_details(soup)
        el_group = []
        if target_id:
            el = soup.find(id=target_id)
            if el:
                el_group.append(el)
        if target_class:
            el = soup.find(class_=target_class)
            if el:
                el_group.append(el)
        if target_tag:
            el = soup.find(target_tag)
            if el:
                el_group.append(el)
        target_element = None
        for el in el_group:
            if el.find("a"):
                target_element = el
                break
        if not target_element and el_group:
            target_element = el_group[0]
        if not target_element:
            print(f"Target tags unavailable: {url}")
        else:
            target_links_group = target_element.find_all("a", recursive=True)
            return status_code, title, meta_desc, canonical_link, target_links_group
        return status_code, title, meta_desc, canonical_link, []
    except RequestException as e:
        print(f"Error requesting {url}: {e}")
        return 0, "", "", "", []

def within_crawl_depth(link_depth, crawl_depth):
    return link_depth <= crawl_depth

# get user input URL
def get_crawl_seed(const):
    while True:
        init_prompt = helpers.custom_input("Enter property initials as above: ").upper()
        if init_prompt == 'XX':
            user_url = helpers.custom_input("Please enter a valid URL: ")
            if not re.match(r"^https?://", user_url):
                use_https = input("The input is missing a protocol scheme. Use HTTPS? (Y)es or (N)o?: ").strip().lower()
                if use_https in ['no', 'n']:
                    protocol = input("Please indicate the proper protocol to use (http/https) or type 'None': ").strip()
                    if protocol.lower() != 'none':
                        user_url = f"{protocol}://{user_url}"
                    else:
                        print("Invalid input. Assuming HTTPS protocol.")
                        user_url = f"https://{user_url}"
                elif use_https in ['yes', 'y']:
                    user_url = f"https://{user_url}"
                else:
                    print("Invalid choice. Assuming HTTPS protocol.")
                    user_url = f"https://{user_url}"
            if not is_valid_url(user_url):
                print("Invalid URL. Please enter a valid URL.")    
            print("Processing the following URL:", user_url)
            return init_prompt, user_url
        elif len(init_prompt) <= 3 and init_prompt in const.PROPS:
            ref_url = const.PROPS[init_prompt]
            print(f"The winner is... {ref_url}")
            return init_prompt, ref_url 
        else:
            print("Invalid input. Please enter a 2-letter character designation.\n")

# get file name from user
def get_file_name():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = helpers.custom_input(f"Enter desired file name now or leave empty for default (url-crawl-output_{timestamp}.csv): ").strip()
    if not file_name:
        file_name = f"url-crawl-output_{timestamp}.csv"
    else:
        file_name = f"{file_name}_{timestamp}.csv"
    # initalize a new file with headers if none
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            file.write('URL,Status Code,Title,Meta Description,Canonical Link,Source\n')
    return file_name

# save output to a file
def save_to_file(file_name, data):
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        for row in data:
            # double quotes to handle commas
            row = ['"{}"'.format(value) for value in row]
            file.write(','.join(row) + '\n')

def crawl(headers, init_prompt, url_seed, target_tag, target_id, target_class, crawl_depth, file_name):
    # init list with the seed URL, depth, and source (None for seed URL)
    to_crawl = [(url_seed, 0, None)]
    output_data = []
    crawled_urls = set()
    counted_urls = 0
    total_errors = 0
    print(f"\nCrawl seed: {url_seed}\n"
          f"Target tag: {target_tag}\n"
          f"Target ID: {target_id}\n"
          f"Target class: {target_class}\n"
          f"Crawl depth: {crawl_depth}\n"
          f"File name: {file_name}\n")
    input("Press Enter to begin...")
    start_time = time.time()
    while to_crawl:
        target_url, current_depth, source_url = to_crawl.pop(0)
        if current_depth <= crawl_depth and target_url not in crawled_urls:
            status_code, title, meta_desc, canonical_link, target_links_group = get_page_info(
                target_url, headers, target_tag, target_id, target_class)
            if not is_valid_url(target_url):
                print(f"Invalid URL: {target_url}")
                continue
            # errors and 404s
            if status_code == 404:
                print(f"404 Error: {target_url}")
                output_data.append([target_url, f"{status_code}", "", "", "", source_url])
                save_to_file(file_name, [[target_url, f"{status_code}", title, meta_desc, canonical_link, source_url]])
                crawled_urls.add(target_url)
                total_errors += 1
                continue
            elif status_code >= 400 and status_code != 404:
                print(f"Error, Client or Server: {status_code} | URL: {target_url}")
                output_data.append([target_url, f"{status_code}", "", "", "", source_url])
                crawled_urls.add(target_url)
                total_errors += 1
                continue
            counted_urls += 1
            print(f"Saved to file: {target_url}")
            # add delay for 403, else normal delay
            if status_code == 403:
                print(f"Received 403 status code. Adding a longer delay.")
                time.sleep(5)
            else:
                time.sleep(1)
            # log every 50 URLs
            if counted_urls % 50 == 0:
                print(f"Analysis in progress... counted {counted_urls} URLs so far.")
            output_data.append([target_url, f"{status_code}", title, meta_desc, canonical_link, source_url])
            save_to_file(file_name, [[target_url, f"{status_code}", title, meta_desc, canonical_link, source_url]])
            crawled_urls.add(target_url)
            # extract links and track source
            for link in target_links_group:
                href = link.get("href", "")
                if not href:
                    continue
                if any(href.startswith(s) for s in ("tel:", "mailto:", "#")) or "descpage" in href:
                    continue
                absolute_link = urljoin(target_url, href)
                parsed_link = urlparse(absolute_link)
                if parsed_link.netloc == urlparse(url_seed).netloc:
                    to_crawl.append((absolute_link, current_depth + 1, target_url))
    print(f"\nIdentified {counted_urls} links, {total_errors} errors were found | Saved output to {file_name}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time}")

def init_menu(const_file=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36-X"
    }
    const = load_const_module(const_file)
    for designation, url in const.PROPS.items():
        print(f'{designation}: {url}')
    print("Web Crawler by JDT\n"
          "Current functionality: NAV links only\n"
          "Testing functionality: CONTENT links only\n"
          "Excluding 'descpages', contact links, and jumplinks(#)")
    init_prompt, url_seed = get_crawl_seed(const)
    target_tag, target_id, target_class = get_targets(init_prompt, url_seed, const)
    crawl_depth = get_crawl_depth()
    file_name = get_file_name()
    crawl(headers, init_prompt, url_seed, target_tag, target_id, target_class, crawl_depth, file_name)

@helpers.handle_exceptions
def main():
    parser=argparse.ArgumentParser(
        prog="Simple Web Link Crawler",
        description="Crawl a website for links based on parameters defined in the const.py file.",
        epilog="Developed by JDT",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-c", "--const",
        help="Use a custom constant.py file for crawling parameters.",
    )
    args=parser.parse_args()
    init_menu(const_file=args.const)

if __name__ == '__main__':
    main()
