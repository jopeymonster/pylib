import time
import os
import sys
import re
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse

# 3p imports
from tabulate import tabulate

# my imports

# exceptions wrapper
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            print_error(func.__name__, e)
        except ValueError as e:
            print_error(func.__name__, e)
        except KeyboardInterrupt as e:
            print_error(func.__name__, e)
        except FileNotFoundError as e:
            print_error(func.__name__, e)
        except AttributeError as e:
            print_error(func.__name__, )
        except Exception as e:
            print_error(func.__name__, e)
    def print_error(func_name, error):
        print(f"\nError in function '{func_name}': {repr(error)} - Exiting...\n")
    return wrapper

# user error logging
def user_error(err_type):
    if err_type == 1:
        sys.exit("Problem with MAIN loop.")
    if err_type == 2:
        sys.exit("Invalid input.")
    elif err_type in [3,4]:
        sys.exit("Problem with output data.")

# generate timestamp
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
now_time = f"The current timedate is {timestamp}"
print(now_time)

# start time
start_time = time.time()

# time output
end_time = time.time()
execution_time = end_time - start_time
print(f"Total execution time: {execution_time}")

# throttle batching
some_items = []
batch_size = 50  # Adjust as needed
for i in range(0, len(some_items), batch_size):
    batch_ids = some_items[i:i+batch_size]

# retries
max_retries = 3
for retry_count in range(max_retries):
    try:
        # Make API request
        break  # Break out of the loop if successful
    except Exception as e:
        print(f"Error: {repr(e)} - Retrying...")
        if retry_count == max_retries - 1:
            print("Max retries reached. Exiting...")
            sys.exit(1)

# tabluate
def tabluate_output(data):
    columns = ['field1', 'field2', 'field3', 'field4', 'field5'] # add fields as needed   
    table_data = [
        {col: entry.get(col, '') for col in columns}
        for entry in data
    ]
    table = tabulate(table_data, headers='keys', tablefmt="simple_grid")
    print(table)

# validate url
url = "https://www.example.com"
if urlparse(url).scheme and urlparse(url).netloc:
    print(f"{url} is a valid URL.")
else:
    print(f"{url} is not a valid URL.")

# validate URL as function
def is_valid_url(url):
    result = urlparse(url)
    return all([result.scheme, result.netloc])

# URL input
def url_input(user_url):
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


# validate file and file location
saved_file = "/path/to/file/file.txt"
if os.path.exists(saved_file):
    print(f"{saved_file} exists!")
if os.path.isfile(saved_file):
    print(f"The file is saved here: {os.path.abspath(saved_file)}")
# if os.path.exists(saved_file) and os.path.isfile(saved_file):
# print(f"{saved_file} found at {os.path.abspath(saved_file)}")


# validate file+file location as function
saved_file = "/path/to/file/file.txt"
def validate_file_location(saved_file):
    return os.path.exists(saved_file) and os.path.isfile(saved_file)


"""
Validate date format and if within range parameters

args:
[0] - start_date
[1] - end_date
[2] - time range segmentation

Example usage
validate_date('2024/04/01', '2024/04/30', 'LAST_MONTH')
"""
# Initialize the DURING_TIME_SEG dictionary as a constant
DURING_TIME_SEG = {
    '1': 'LAST_7_DAYS',
    '2': 'LAST_BUSINESS_WEEK',
    '3': 'THIS_MONTH',
    '4': 'LAST_MONTH',
    '5': 'LAST_14_DAYS',
    '6': 'LAST_30_DAYS',
    '7': 'THIS_WEEK_SUN_TODAY',
    '8': 'LAST_WEEK_SUN_SAT',
}

def is_valid_date(date_str):
    """Check if the date string is in the format YYYY/MM/DD."""
    try:
        datetime.datetime.strptime(date_str, "%Y/%m/%d")
        return True
    except ValueError:
        return False

def is_start_of_week(date_str):
    """Check if the date is the start of a week (Monday)."""
    date = datetime.datetime.strptime(date_str, "%Y/%m/%d")
    return date.weekday() == 0  # Monday

def is_end_of_month(date_str):
    """Check if the date is the end of a month."""
    date = datetime.datetime.strptime(date_str, "%Y/%m/%d")
    next_day = date + datetime.timedelta(days=1)
    return next_day.day == 1

def validate_date(start_date, end_date, time_seg):
    # Validate start_date and end_date
    if not is_valid_date(start_date):
        print("Invalid date:", start_date)
        return
    if not is_valid_date(end_date):
        print("Invalid date:", end_date)
        return

    # Validate time_seg
    if time_seg not in DURING_TIME_SEG.values():
        print("Invalid time segment:", time_seg)
        return

    # Check for week-related conditions
    if 'week' in time_seg.lower():
        if not is_start_of_week(start_date):
            print(f"Invalid start date and segment combination: ({start_date}, {time_seg})")
            return

    # Check for month-related conditions
    if 'month' in time_seg.lower():
        if not is_end_of_month(end_date):
            print(f"Invalid end date and segment combination: ({end_date}, {time_seg})")
            return

    print("Dates and time segment are valid.")

""""""


"""
Transform variables as literals

"""
def assign_variable(variables, var_name, value):
    variables[var_name] = f"'{value}'"

# Dictionary to hold variables
variables = {}
# Assign variables
assign_variable(variables, "dynamic_var", 42)
# Access the variable
print(variables["dynamic_var"])  # Output: '42'

"""
Long form logic for literal transformation
"""
# Dictionary to hold variables
variables = {}
# Original variables
var_name = "dynamic_var"
value_to_assign = 42
# Assign the value to a key in the dictionary, surrounding the value with single quotes
variables[var_name] = f"'{value_to_assign}'"
# Access the variable
print(variables["dynamic_var"])  # Output: '42'


"""capture parameters"""
import re
def match_url(url):
  """Matches the given url against the regex."""
  match = re.match(r'\/\?(ccode|pcode)=(.*)', url)
  if match:
    return match.groups()
  else:
    return None

"""example"""
if __name__ == '__main__':
  url = '/?ccode=12345&pcode=54321'
  ccode, pcode = match_url(url)
  print(ccode, pcode)


"""regex target page capture parameter"""
import re
def match_url(url):
  """Matches the given url against the regex."""
  match = re.match(r'\/productvideo\.html\?pcode=(.*)|\/categoryvideo\.html\?pcode=(.*)', url)
  if match:
    return match.group(1)
  else:
    return None

"""example"""
if __name__ == '__main__':
  url = '/productvideo.html?pcode=12345'
  pcode = match_url(url)
  print(pcode)