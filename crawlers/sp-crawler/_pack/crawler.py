# crawler.py

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, initial_url, crawl_depth, file_name):
        self.initial_url = initial_url
        self.crawl_depth = crawl_depth
        self.file_name = file_name
        self.output_data = []
        self.crawled_urls = set()
        self.counted_urls = 0
        self.total_errors = 0
        self.to_crawl = [(self.initial_url, 0)]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
        }

    def get_response_data(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None

    def extract_info(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical_link = canonical_tag["href"].strip() if canonical_tag else "No canonical present"
        return title, canonical_link

    def get_meta_description(self, url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag and "content" in meta_tag.attrs:
                return meta_tag["content"].strip()
            return "No meta description"
        except requests.exceptions.RequestException as e:
            return str(e)

    def get_status_code(self, url):
        try:
            response = requests.head(url)
            return response.status_code
        except requests.exceptions.RequestException as e:
            return str(e)

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def within_crawl_depth(self, link_depth):
        return link_depth <= self.crawl_depth

    def crawl_url(self, current_url, current_depth):
        html_content = self.get_response_data(current_url)
        status_code = self.get_status_code(current_url)
        title, canonical_link = self.extract_info(html_content)
        description = self.get_meta_description(current_url)

        if not self.is_valid_url(current_url):
            print(f"Invalid URL: {current_url}")
            return

        if status_code >= 400:
            print(f"Error, Client or Server: {status_code} | URL: {current_url}")
            self.total_errors += 1
        else:
            self.counted_urls += 1
            print(f"{current_url} - saved to file")
            if status_code == 403:
                print(f"Received 403 status code. Adding a longer delay.")
                time.sleep(5)
            else:
                time.sleep(1)
            if self.counted_urls % 50 == 0:
                print(f"Analysis in progress... counted {self.counted_urls} URLs so far.")

        self.output_data.append([
            current_url, f"{status_code}", title, description, canonical_link
        ])

        self.crawled_urls.add(current_url)

        soup = BeautifulSoup(html_content, "html.parser")
        for link in soup.find_all("a", href=True):
            link = link.get('href')

            if "#" in link or link.startswith("tel:"):
                continue

            if link and (link.endswith(".html") or link.endswith(".htm") or not '.' in link):
                absolute_link = urljoin(current_url, link)

                if self.within_crawl_depth(current_depth + 1) and urlparse(absolute_link).netloc == urlparse(self.initial_url).netloc:
                    self.to_crawl.append((absolute_link, current_depth + 1))

    def crawl(self):
        while self.to_crawl:
            current_url, current_depth = self.to_crawl.pop(0)
            if current_depth <= self.crawl_depth and current_url not in self.crawled_urls:
                self.crawl_url(current_url, current_depth)
