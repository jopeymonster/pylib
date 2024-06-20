#use: download_images('https://example.com', '.example-class', load_more_element='#load-more-button', filename='my_links.csv')


import requests
import csv
from bs4 import BeautifulSoup


def download_images(url, class_name, load_more_element=None, filename="image_links.csv"):
    """
    Downloads all images from img tag links in the specified class
    or section of the webpage, and saves their URLs to a CSV file.

    :param url: URL of the webpage to crawl
    :param class_name: Name of the class or section of the webpage to target
    :param load_more_element: (Optional) CSS selector of a HTML element that can be clicked to load more images
    :param filename: (Optional) Name of the output CSV file
    :return: None
    """
    img_links = []

    # Crawl the initial page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    img_tags = soup.select(f"{class_name} img")
    for img in img_tags:
        img_link = img.get("src")
        if img_link:
            img_links.append(img_link)

    # Load more images if load_more_element is provided
    if load_more_element:
        while True:
            load_more_button = soup.select_one(load_more_element)
            if not load_more_button:
                break
            next_page_response = requests.get(url + load_more_button["href"])
            soup = BeautifulSoup(next_page_response.content, "html.parser")
            next_page_img_tags = soup.select(f"{class_name} img")
            for img in next_page_img_tags:
                img_link = img.get("src")
                if img_link:
                    img_links.append(img_link)

    # Write the links to a CSV file
    with open(filename, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["img_link"])
        for img_link in img_links:
            writer.writerow([img_link])
            print(f"Image link '{img_link}' written to '{filename}'")
