import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import os
import requests
import csv
from bs4 import BeautifulSoup


def write_to_csv(img_links, filename):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        for link in img_links:
            writer.writerow([link])
            print(f"{link} has been added to {filename}")
        print(f"Total image links in {filename}: {len(img_links)}")


def extract_img_links(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    img_links = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            img_links.append(src)
            print(f"{src} extracted from <img> tag")
    return img_links


def load_more(driver, load_more):
    if load_more:
        try:
            driver.find_element_by_css_selector(load_more).click()
            print(f"{load_more} activated")
        except:
            print(f"No more {load_more} to load")


def download_images(url, class_name, load_more=None, filename='image_links.csv'):
    img_links = set()
    count = 0

    # Load the page HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image links in the page HTML
    img_tags = soup.select(class_name + ' img')
    for img_tag in img_tags:
        img_links.add(img_tag['src'])

    # Check if there are additional image links to be loaded
    if load_more:
        while True:
            # Find the "load more" HTML element and click it
            load_more_element = soup.select_one(load_more)
            if not load_more_element:
                break

            # Load the next set of HTML with the additional image links
            next_url = urljoin(url, load_more_element['href'])
            response = requests.get(next_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all image links in the new HTML and add them to the set
            img_tags = soup.select(class_name + ' img')
            for img_tag in img_tags:
                img_links.add(img_tag['src'])

    # Write the image links to a CSV file
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image Links'])

        for img_link in img_links:
            writer.writerow([img_link])
            count += 1
            print(f'{count} image link(s) written to {filename}')

    print(f'Finished writing {count} image link(s) to {filename}')



if __name__ == '__main__':
    url = input("Enter the URL to crawl: ")
    class_name = input("Enter the class name of the images to extract: ")
    load_more = input(
        "Enter the CSS selector of the load more button (optional): ")
    filename = input(
        "Enter the filename for the image links (default is image_links.csv): ") or "image_links.csv"
    download_images(url, class_name, load_more, filename)

