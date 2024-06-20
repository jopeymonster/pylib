# Import the custom_input module to override the built-in input function
from modules import jdt_inputs
import re

def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

def url_input():
    user_url = input("Please enter a valid URL: ")
    if not re.match(r"^https?://", user_url):
        use_https = input("The input is missing a protocol scheme. Use HTTPS? (Y)es or (N)o?: ").strip().lower()
        if use_https in ['no', 'n']:
            protocol = input("Please indicate the proper protocol to use (http/https) or type 'None': ").strip()
            if protocol.lower() != 'none':
                user_url = f"{protocol}://{user_url}"
            else:
                print("Invalid input. Assuming HTTPS protocol.")
                user_url = f"https://{user_url}"
        elif use_https in ['yes', 'y']:
            user_url = f"https://{user_url}"
        else:
            print("Invalid choice. Assuming HTTPS protocol.")
            user_url = f"https://{user_url}"
    if not is_valid_url(user_url):
        print("Invalid URL. Please enter a valid URL.")
    print("Processing the following URL:", user_url)
    return user_url

def main():
    url_input()

if __name__ == "__main__":
    main()
