import os
import requests
from bs4 import BeautifulSoup

# specify the URL of the webpage to crawl
url = "https://www.example.com"

# create a directory to store the downloaded images
if not os.path.exists("images"):
    os.makedirs("images")

# send a request to the URL and get the HTML content
response = requests.get(url)
html_content = response.content

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# find all image tags on the webpage
img_tags = soup.find_all("img")

# iterate over each image tag and download the image
for img in img_tags:
    img_url = img["src"]
    if "specific_image_name" in img_url:
        img_name = img_url.split("/")[-1]
        img_path = os.path.join("images", img_name)
        with open(img_path, "wb") as f:
            f.write(requests.get(img_url).content)
            print(f"Downloaded {img_name}")
