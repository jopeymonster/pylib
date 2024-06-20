#use: download_images('https://example.com', '.example-class', load_more='#load-more-button')

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_images(url, class_element=None, wait_time=5, load_more=None):
    # Set up Chrome web driver with Selenium
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for lazy loading images and additional image source markup to load
    time.sleep(wait_time)

    # Find all <img> tags in the specified class or in the body section
    if class_element:
        images = driver.find_elements(By.CSS_SELECTOR, class_element + ' img')
    else:
        images = driver.find_elements(By.CSS_SELECTOR, 'body img')

    # Download the images to a specified directory and print their URLs to the console
    for img in images:
        img_url = img.get_attribute('src')
        if img_url.startswith(('http', 'https')):
            filename = os.path.join('images', img_url.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(img_url).content)
            print(f'Downloaded {filename}')
            print(f'Image URL: {img_url}')

    # Click on an element to load additional images, if specified
    if load_more:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, load_more)))
        element.click()
        time.sleep(wait_time)

        # Find any new <img> tags that have been added after clicking the element
        if class_element:
            images = driver.find_elements(By.CSS_SELECTOR, class_element + ' img')
        else:
            images = driver.find_elements(By.CSS_SELECTOR, 'body img')

        # Download the new images to the specified directory and print their URLs to the console
        for img in images:
            img_url = img.get_attribute('src')
            if img_url.startswith(('http', 'https')):
                filename = os.path.join('images', img_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(requests.get(img_url).content)
                print(f'Downloaded {filename}')
                print(f'Image URL: {img_url}')

    # Close the web driver
    driver.quit()
