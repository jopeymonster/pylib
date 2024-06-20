#use: download_images('https://example.com', '.example-class', load_more='#load-more-button', filename='my_links.csv')

import requests
from bs4 import BeautifulSoup
import os
import csv

def write_to_csv(url_list, filename='image_links.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image URLs'])
        count = 0
        for url in url_list:
            writer.writerow([url])
            count += 1
            print(f"Image URL #{count}: {url}")
    print(f"Image URLs written to {filename}")

def get_image_links(url, class_element, load_more=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_tags = soup.select(class_element + ' img')
    image_links = [img['src'] for img in image_tags]
    if load_more:
        while soup.select_one(load_more):
            next_page_link = soup.select_one(load_more)['href']
            next_page = requests.get(next_page_link, headers=headers)
            soup = BeautifulSoup(next_page.content, 'html.parser')
            image_tags = soup.select(class_element + ' img')
            image_links += [img['src'] for img in image_tags]
    return image_links

def download_images(url, class_element, load_more=None):
    image_links = get_image_links(url, class_element, load_more)
    filename = 'image_links.csv'
    write_to_csv(image_links, filename)

