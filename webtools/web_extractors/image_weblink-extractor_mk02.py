#use: get_img_links('https://example.com', '.example-class', load_more='#load-more-button', filename='my_links.csv')

import requests
from bs4 import BeautifulSoup
import csv

def get_img_links(url, class_name, load_more=None, filename="image_links.csv"):
    img_links = []
    page = 1
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        while True:
            print(f"Processing page {page}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            img_tags = soup.find_all("img", {"class": class_name})
            
            for img in img_tags:
                img_link = img.get("src")
                if img_link not in img_links:
                    writer.writerow({"link": img_link})
                    img_links.append(img_link)
                    print(f"Added {img_link} to {filename}. Total count: {len(img_links)}")
            
            if not load_more:
                break
            
            load_more_button = soup.find(load_more)
            if not load_more_button:
                break
                
            url = load_more_button.get("href")
            page += 1
    print(f"Total unique image links found and written to {filename}: {len(img_links)}")
