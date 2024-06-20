import os
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the URL of the webpage to scrape
url = "https://schools.mybrightwheel.com/students/1e4ba796-bb24-4d86-8626-8256f011250f/feed"

# Set up the Selenium webdriver
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 10)

# Find the "Load More" button and click it until all content is loaded
while True:
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'load-button')]")))
        load_more_button.click()
    except:
        break

# Parse the HTML response with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all div elements with class "activity-card-module-content-"
# divs = soup.find_all("div", class_=lambda x: x and x.startswith("activity-card-module-content-"))
divs = soup.find_all("div", class_=re.compile(r"activity-card-module-content-\w+"))

# Create a folder to store the downloaded images
folder_name = "brightwheel_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Iterate over the div elements and extract the image URLs
for i, div in enumerate(divs):
    # Get the image URL from the "data-src" attribute
    img_url = div["data-src"]
    
    # Send a GET request to the image URL and save the image to a file
    img_data = requests.get(img_url).content
    file_name = f"image_{i}.jpg"
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "wb") as f:
        f.write(img_data)
        print(f"Image {i} downloaded and saved as {file_name} in folder {folder_name}")

# Close the webdriver
driver.quit()
