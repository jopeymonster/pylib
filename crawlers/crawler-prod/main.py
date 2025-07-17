# imports
import sys
import os
import time
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Doctype
from urllib.parse import urljoin, urlparse
from _pack import const
import helpers

# prop list
def prop_list():
    for designation, url in const.PROPS.items():
        print(f'{designation}: {url}')

# validate URL
def is_valid_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc])

def get_crawl_depth():
    while True:
        crawl_depth_input = input("Indicate desired crawl depth (as an integer) or leave blank to crawl the entire site: ")
        if crawl_depth_input.strip().isdigit():
            return int(crawl_depth_input)
        elif not crawl_depth_input.strip():
            return float('inf')
        else:
            print("Invalid input. Please enter a valid integer or leave it blank.")

# new get_target test
def get_targets(init_prompt, url):
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
        tag_choice = input("1 or 2: ")
        if tag_choice == '1' or tag_choice == '2':
            break
        else:
            print("Invalid input, please select 1 or 2")
    # call handle_tag_choice to get the target qualifiers
    # print(f"Tag choice: {tag_choice} | Init prompt: {init_prompt}")
    target_tag, target_id, target_class = handle_tag_choice(tag_choice, init_prompt)
    return target_tag, target_id, target_class

def handle_tag_choice(tag_choice, init_prompt):
    if tag_choice == '1':
        target_tag = const.NAVTAGS.get(init_prompt, "")
        target_id = const.NAVIDS.get(init_prompt, "")
        target_class = const.NAVCLASSES.get(init_prompt, "")
    elif tag_choice =='2':
        target_tag = const.CONT_TAGS.get(init_prompt, "")
        target_id = const.CONT_IDS.get(init_prompt, "")
        target_class = const.CONT_CLASSES.get(init_prompt, "")
    # print("Processed targets: ")
    # print(target_tag, target_id, target_class)
    return target_tag, target_id, target_class

def get_page_details(soup):
    title = soup.title.string.strip() if soup.title and soup.title.string is not None else "No title"
    canonical_tag = soup.head.find("link", rel="canonical")
    canonical_link = canonical_tag["href"].strip() if canonical_tag and canonical_tag.get("href") is not None else "No canonical present"
    meta_tag = soup.head.find("meta", attrs={"name": "description"})
    meta_desc = meta_tag["content"].strip() if meta_tag and "content" in meta_tag.attrs and meta_tag.get("content") is not None else "No meta description"
    return title, meta_desc, canonical_link

def get_page_info(url, headers, target_tag, target_id, target_class):
    response = requests.get(url, headers=headers, timeout=20)
    # response.raise_for_status()
    status_code = response.status_code
    if status_code in [404,406]:
        return status_code, "","","",[] 
    target_links_group = []
    page_markup = response.content
    soup = BeautifulSoup(page_markup, "html.parser")
    # check for doctype declaration
    doctype_pattern = re.compile(br"^\s*(<!--.*?-->\s*)*<!DOCTYPE html>", re.IGNORECASE | re.DOTALL)
    has_doctype = bool(doctype_pattern.match(page_markup))
    if not has_doctype:
        print(f"DTD missing: {url}")
        return status_code, "","","",[]
    # missing <head> tag
    head_tag = soup.find("head")
    if head_tag is None:
        print(f"<head> tag not found: {url}")
        title, meta_desc, canonical_link = get_page_details(soup)
    else:   
        title, meta_desc, canonical_link = get_page_details(soup)
    target_element = None
    # find the element by ID if target_id exists
    if target_id:
        target_element = soup.find(id_=target_id)
    # if target element is still not found, try to find it by class if target_class
    if target_element is None and target_class:
        target_element = soup.find(class_=target_class)
    # If target element is still not found, try to find it by tag if target_tag
    if target_element is None and target_tag:
        target_element = soup.find(target_tag)
    # Check if target_element is still None after all attempts
    if target_element is None:
        print(f"Target tags unavailable: {url}")
        title, meta_desc, canonical_link = get_page_details(soup)

    else:
        # If target_element is found, get all anchor tags within it
        target_links = target_element.find_all("a", recursive=True)
        target_links_group.extend(target_links)

    return status_code, title, meta_desc, canonical_link, target_links_group

def within_crawl_depth(link_depth, crawl_depth):
    return link_depth <= crawl_depth

# get user input URL
def get_crawl_seed():
    prop_list()
    print("Web Crawler by JDT\n"
          "Current functionality: NAV links only\n"
          "Testing functionality: CONTENT links only\n"
          "Excluding 'descpages', contact links, and jumplinks(#)")
    while True:
        init_prompt = input("Enter property initials as above: ").upper()
        if init_prompt == 'EX':
            sys.exit("Exiting...")
        elif init_prompt == 'XX':
            user_url = input("Please enter a valid URL: ")
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
        # evaluate elif needed
        # elif is_valid_url(init_prompt):
        #     print(f"The winner is...{init_prompt}")
        #     return init_prompt, init_prompt 
        else:
            print("Invalid input. Please enter a 2-letter character designation.\n")

# get file name from user
def get_file_name():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = input(f"Enter desired file name now or leave empty for default (url-crawl-output_{timestamp}.csv): ").strip()
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

def crawl():    
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36-X"}
    init_prompt, url_seed = get_crawl_seed()
    target_tag, target_id, target_class = get_targets(init_prompt, url_seed)
    crawl_depth = get_crawl_depth()
    file_name = get_file_name()
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
                link = link.get("href", "No href attribute")
                if "#" in link or link.startswith("tel:") or re.search(r'descpage', link):
                    continue
                if link and (link.endswith(".html") or link.endswith(".htm") or not '.' in link):
                    absolute_link = urljoin(target_url, link)
                    if within_crawl_depth(current_depth + 1, crawl_depth) and urlparse(absolute_link).netloc == urlparse(url_seed).netloc:
                        to_crawl.append((absolute_link, current_depth + 1, target_url))
    print(f"\nIdentified {counted_urls} links, {total_errors} errors were found | Saved output to {file_name}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time}")

@helpers.handle_exceptions
def main():
    while True:
        crawl()

if __name__ == '__main__':
    main()
