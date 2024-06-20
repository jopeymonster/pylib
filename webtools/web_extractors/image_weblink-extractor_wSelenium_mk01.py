import os
import time
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_images(url, class_element=None, wait_time=5, load_more=None, csv_filename='image_links.csv'):
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

    # Write the image URLs to a CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image URL'])

        for img in images:
            img_url = img.get_attribute('src')
            if img_url.startswith(('http', 'https')):
                writer.writerow([img_url])
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

        # Write the new image URLs to the CSV file
        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for img in images:
                img_url = img.get_attribute('src')
                if img_url.startswith(('http', 'https')):
                    writer.writerow([img_url])
                    print(f'Image URL: {img_url}')

    # Close the web driver
    driver.quit()
