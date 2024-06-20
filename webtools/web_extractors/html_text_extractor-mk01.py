#use: python html_to_text_converter.py
import requests
import os
from bs4 import BeautifulSoup

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style tags
    for script in soup(["script", "style"]):
        script.extract()

    # Remove footer and header tags
    for footer in soup(["footer", "header"]):
        footer.extract()

    # Get all text from body tags
    body_text = soup.body.get_text()

    # Remove excess white space
    body_text = " ".join(body_text.split())

    # Remove non-alphanumeric characters
    body_text = ''.join(e for e in body_text if e.isalnum() or e.isspace())

    # Filter out short sentences
    body_text = ' '.join(filter(lambda x: len(x) > 50, body_text.split('.')))

    return body_text


def download_html(url):
    response = requests.get(url)
    return response.content.decode('utf-8')


def main():
    # Get HTML from URL or file
    html = ''
    while html == '':
        input_type = input('Enter "url" to input HTML from a URL, "file" to input HTML from a file: ')
        if input_type == 'url':
            url = input('Enter the URL to download HTML from: ')
            html = download_html(url)
        elif input_type == 'file':
            file_path = input('Enter the file path to the HTML file: ')
            with open(file_path, 'r') as f:
                html = f.read()

    # Extract text from HTML
    text = extract_text_from_html(html)

    # Get default directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_dir = os.path.join(script_dir, 'testingoutput')

    # Define default file_name
    default_name = "extracted_text"

    # Save to file
    save_dir = input(
        f"Enter the directory to save the text file in (default: {default_dir}): ") or default_dir
    file_name = input(
        f"Enter a name for the text file (default: {default_name}): ") or default_name
    file_path = os.path.join(save_dir, file_name)
    with open(file_path, 'w') as f:
        f.write(text)
    print('Text file saved at', file_path)


if __name__ == '__main__':
    main()
