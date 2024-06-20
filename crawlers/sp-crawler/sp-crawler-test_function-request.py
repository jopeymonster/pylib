import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys

# left menu
NAVTAGS = {
    'SW': ('nav'),
    'TW': ('mobile_content', 'l-content-menu'),
    'TE': ('mobile_content', 'l-content-menu'),
    'TO': ('mobile_content', 'l-content-menu'),
    'TK': ('mobile_content', 'l-content-menu'),
    'RW': ('mobile_content', 'l-content-menu'),
    'RE': ('mobile_content', 'l-content-menu'),
    'RA': ('mobile_content', 'l-content-menu'),
    'RD': ('mobile_content', 'l-content-menu'),
    'IC': ('mobile_content', 'l-content-menu'),
    'IW': ('mobile_content', 'l-content-menu'),
    'DW': ('mobile_content', 'l-content-menu'),
    'RB': ('mobile_content', 'l-content-menu'),
    'TP': ('mobile_content', 'l-content-menu'),
    'TA': ('mobile_content', 'l-content-menu'),
    'PA': ('mobile_content', 'l-content-menu'),
}

NAVIDS = {
    'SW': ('main_wrap', 'lnav'),
    'TW': ('mobile_content', 'l-content-menu'),
    'TE': ('mobile_content', 'l-content-menu'),
    'TO': ('mobile_content', 'l-content-menu'),
    'TK': ('mobile_content', 'l-content-menu'),
    'RW': ('mobile_content', 'l-content-menu'),
    'RE': ('mobile_content', 'l-content-menu'),
    'RA': ('mobile_content', 'l-content-menu'),
    'RD': ('mobile_content', 'l-content-menu'),
    'IC': ('mobile_content', 'l-content-menu'),
    'IW': ('mobile_content', 'l-content-menu'),
    'DW': ('mobile_content', 'l-content-menu'),
    'RB': ('mobile_content', 'l-content-menu'),
    'TP': ('mobile_content', 'l-content-menu'),
    'TA': ('mobile_content', 'l-content-menu'),
    'PA': ('mobile_content', 'l-content-menu'),
}

NAVCLASSES = {
    'SW': ('lnav_main', 'lnav_menu'),
    'TW': ('mobile_content', 'l-content-menu'),
    'TE': ('mobile_content', 'l-content-menu'),
    'TO': ('mobile_content', 'l-content-menu'),
    'TK': ('mobile_content', 'l-content-menu'),
    'RW': ('mobile_content', 'l-content-menu'),
    'RE': ('mobile_content', 'l-content-menu'),
    'RA': ('mobile_content', 'l-content-menu'),
    'RD': ('mobile_content', 'l-content-menu'),
    'IC': ('mobile_content', 'l-content-menu'),
    'IW': ('mobile_content', 'l-content-menu'),
    'DW': ('mobile_content', 'l-content-menu'),
    'RB': ('mobile_content', 'l-content-menu'),
    'TP': ('mobile_content', 'l-content-menu'),
    'TA': ('mobile_content', 'l-content-menu'),
    'PA': ('mobile_content', 'l-content-menu'),
}

CONT_TAGS = {
    'SW': ('body'),
    'TW': ('mobile_content', 'l-content-area'),
    'TE': ('mobile_content', 'l-content-area'),
    'TO': ('mobile_content', 'l-content-area'),
    'TK': ('mobile_content', 'l-content-area'),
    'RW': ('mobile_content', 'l-content-area'),
    'RE': ('mobile_content', 'l-content-area'),
    'RA': ('mobile_content', 'l-content-area'),
    'RD': ('mobile_content', 'l-content-area'),
    'IC': ('mobile_content', 'l-content-area'),
    'IW': ('mobile_content', 'l-content-area'),
    'DW': ('mobile_content', 'l-content-area'),
    'RB': ('mobile_content', 'l-content-area'),
    'TP': ('mobile_content', 'l-content-area'),
    'TA': ('mobile_content', 'l-content-area'),
    'PA': ('mobile_content', 'l-content-area'),
}
CONT_IDS = {
    'SW': ('content_wrap'),
    'TW': ('mobile_content', 'l-content-area'),
    'TE': ('mobile_content', 'l-content-area'),
    'TO': ('mobile_content', 'l-content-area'),
    'TK': ('mobile_content', 'l-content-area'),
    'RW': ('mobile_content', 'l-content-area'),
    'RE': ('mobile_content', 'l-content-area'),
    'RA': ('mobile_content', 'l-content-area'),
    'RD': ('mobile_content', 'l-content-area'),
    'IC': ('mobile_content', 'l-content-area'),
    'IW': ('mobile_content', 'l-content-area'),
    'DW': ('mobile_content', 'l-content-area'),
    'RB': ('mobile_content', 'l-content-area'),
    'TP': ('mobile_content', 'l-content-area'),
    'TA': ('mobile_content', 'l-content-area'),
    'PA': ('mobile_content', 'l-content-area'),
}

CONT_CLASSES = {
    'SW': (''),
    'TW': ('mobile_content', 'l-content-area'),
    'TE': ('mobile_content', 'l-content-area'),
    'TO': ('mobile_content', 'l-content-area'),
    'TK': ('mobile_content', 'l-content-area'),
    'RW': ('mobile_content', 'l-content-area'),
    'RE': ('mobile_content', 'l-content-area'),
    'RA': ('mobile_content', 'l-content-area'),
    'RD': ('mobile_content', 'l-content-area'),
    'IC': ('mobile_content', 'l-content-area'),
    'IW': ('mobile_content', 'l-content-area'),
    'DW': ('mobile_content', 'l-content-area'),
    'RB': ('mobile_content', 'l-content-area'),
    'TP': ('mobile_content', 'l-content-area'),
    'TA': ('mobile_content', 'l-content-area'),
    'PA': ('mobile_content', 'l-content-area'),
}

# NAV = {
#     'SW': ('nav','lnav', 'lnav_menu'),
#     'TW': ('mobile_content', 'l-content-menu'),
#     'TE': ('mobile_content', 'l-content-menu'),
#     'TO': ('mobile_content', 'l-content-menu'),
#     'TK': ('mobile_content', 'l-content-menu'),
#     'RW': ('mobile_content', 'l-content-menu'),
#     'RE': ('mobile_content', 'l-content-menu'),
#     'RA': ('mobile_content', 'l-content-menu'),
#     'RD': ('mobile_content', 'l-content-menu'),
#     'IC': ('mobile_content', 'l-content-menu'),
#     'IW': ('mobile_content', 'l-content-menu'),
#     'DW': ('mobile_content', 'l-content-menu'),
#     'RB': ('mobile_content', 'l-content-menu'),
#     'TP': ('mobile_content', 'l-content-menu'),
#     'TA': ('mobile_content', 'l-content-menu'),
#     'PA': ('mobile_content', 'l-content-menu'),
# }

# CONTENT = {
#     'SW': ('content_wrap', 'cf'),
#     'TW': ('mobile_content', 'l-content-area'),
#     'TE': ('mobile_content', 'l-content-area'),
#     'TO': ('mobile_content', 'l-content-area'),
#     'TK': ('mobile_content', 'l-content-area'),
#     'RW': ('mobile_content', 'l-content-area'),
#     'RE': ('mobile_content', 'l-content-area'),
#     'RA': ('mobile_content', 'l-content-area'),
#     'RD': ('mobile_content', 'l-content-area'),
#     'IC': ('mobile_content', 'l-content-area'),
#     'IW': ('mobile_content', 'l-content-area'),
#     'DW': ('mobile_content', 'l-content-area'),
#     'RB': ('mobile_content', 'l-content-area'),
#     'TP': ('mobile_content', 'l-content-area'),
#     'TA': ('mobile_content', 'l-content-area'),
#     'PA': ('mobile_content', 'l-content-area'),
# }

PROPS = {
'DW':'https://www.derbywarehouse.com/',
'IC':'https://www.icewarehouse.com/',
'IW':'https://www.inlinewarehouse.com/',
'RB':'https://www.racquetballwarehouse.com/',
'RD':'https://www.ridingwarehouse.com/',
'RW':'https://www.runningwarehouse.com/',
'RA':'https://www.runningwarehouse.com.au/',
'SW':'https://www.skatewarehouse.com/',
'TK':'https://www.tacklewarehouse.com/',
'TO':'https://www.tennisonly.com.au/',
'TW':'https://www.tennis-warehouse.com/',
'TA':'https://www.totalpickleball.com.au/',
'RE':'https://www.runningwarehouse.eu/',
'TE':'https://www.tenniswarehouse-europe.com/',
'TP':'https://www.totalpickleball.com/',
'PA':'https://www.totalpadel.com/'
}

# exceptions
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as _:
            print(f"\nError making request: {repr(_)} - Exiting...\n")
        except ValueError as _:
            print(f"\nInvalid input: {repr(_)} - Exiting...\n")
        except KeyboardInterrupt as _:
            print(f"\nUser Interrupt: {repr(_)} - Exiting...\n")
        except FileNotFoundError as _:
            print(f"\nFile not found: {repr(_)} - Exiting...\n")
        except Exception as _:
            print(f"\nError: {repr(_)} - Exiting...\n")
    return wrapper

def get_targets(init_prompt):
    while True:
        print("1. NAV\n"
              "2. or CONTENT?\n")
        tag_choice = input("1 or 2: ")
        if tag_choice == '1':
            target_tag = NAVCLASSES[init_prompt]
            target_id = NAVIDS[init_prompt]
            target_class = NAVCLASSES[init_prompt]
            break
        elif tag_choice =='2':
            target_tag = CONT_CLASSES[init_prompt]
            target_id = CONT_IDS[init_prompt]
            target_class = CONT_CLASSES[init_prompt]
            break
        else:
            print("Invalid input, please select 1 or 2")
    return target_tag, target_id, target_class

def get_page_info(url, headers, target_tag, target_id, target_class):
    response = requests.get(url, headers=headers, timeout=10)
    # response.raise_for_status()
    status_code = response.status_code
    if status_code == 404:
        return status_code, "","","","",[] 
    page_markup = response.content
    soup = BeautifulSoup(page_markup, "html.parser")
    title = soup.title.string.strip() if soup.title else "No title"
    canonical_tag = soup.head.find("link", rel="canonical", href=True)
    canonical_link = canonical_tag["href"].strip() if canonical_tag else "No canonical present"
    meta_tag = soup.head.find("meta", attrs={"name": "description"})
    meta_desc = meta_tag["content"].strip() if meta_tag and "content" in meta_tag.attrs else "No meta description"
    # Try to find the target element using target_id
    target_element = None
    if target_id:
        target_element = soup.find(id_=target_id)
    # If target_id is not found and target_class is specified, try to find the target element using class
    if target_element is None and target_class:
        target_element = soup.find(class_=target_class)
    # If both target_id and class are not found, try to find the target element using only target_tag
    if target_element is None:
        target_element = soup.find(target_tag)
    # If target element is found, get all anchor tags within it
    target_links_group = []
    if target_element:
        target_links = target_element.find_all("a", recursive=True)
        target_links_group.extend(target_links)
    return status_code, title, meta_desc, canonical_link, target_links_group

# prop list
def prop_list():
    for designation, url in PROPS.items():
        print(f'{designation}: {url}')

# validate a URL
def is_valid_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc])

# get user input URL
def get_crawl_seed():
    prop_list()
    while True:
        init_prompt = input("Enter property initials as above: ").upper()
        if len(init_prompt) == 2 and init_prompt in PROPS:
            print(f"The winner is...{PROPS[init_prompt]}")
            return init_prompt, PROPS[init_prompt]
        elif is_valid_url(init_prompt):
            print(f"The winner is...{init_prompt}")
            return init_prompt, init_prompt
        else:
            print("Invalid input. Please enter a 2-letter character designation or a valid URL.")

@handle_exceptions
def main():
    prop_choice, url_input = get_crawl_seed()
    if not is_valid_url(url_input):
        print("Invalid URL. Please enter a valid URL.")
        sys.exit(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }
    target_tag, target_id, target_class= get_targets(prop_choice)
    print(f"Test Inputs\n" 
          f"URL: {url_input}\n"
          f"Header: {headers}\n"
          f"Link tag target: {target_tag}\n"
          f"Link ID target: {target_id}\n"
          f"Link class: {target_class}\n")
    status_code, title, meta_desc, canonical_link, target_links_group = get_page_info(url_input, headers, target_tag, target_id, target_class)
    # print(f"Status Code: {status_code}\n"
    #      f"Title: {title}\n"
    #      f"Meta Description: {meta_desc}\n"
    #      f"Canonical Link: {canonical_link}\n"
    print(f"Qualified Links:")
    for link in target_links_group:
        target_href = link.get("href", "No href attribute")
        target_text = link.get_text(strip=True)
        print(f"Link Href: {target_href}")
        # print(f"Text: {target_text}")

if __name__ == '__main__':
    main()
