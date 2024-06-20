# example use
# download_images('https://example.com', '.example-class')

import requests
from bs4 import BeautifulSoup
import os

def download_images(url, class_element=None):
    # Create a requests session to get webpage content
    with requests.Session() as session:
        response = session.get(url)
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <img> tags in the specified class or in the body section
        if class_element:
            images = soup.select(class_element + ' img')
        else:
            images = soup.select('body img')

        # Download the images to a specified directory
        for img in images:
            img_url = img.get('src')
            if img_url.startswith(('http', 'https')):
                filename = os.path.join('images', img_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(session.get(img_url).content)
                print(f'Downloaded {filename}')
