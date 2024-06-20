# gmc-feed_status_update

# imports
from __future__ import print_function
import sys
import os
from datetime import datetime
import googleapiclient.errors
from content import _common

# exceptions
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except googleapiclient.errors.HttpError as _:
            print(f"\nAPI request failed: {repr(_)} - Exiting...\n")        
        except ValueError as _:
            print(f"\nInvalid input: {repr(_)} - Exiting...\n")
        except KeyboardInterrupt as _:
            print(f"\nUser Interrupt: {repr(_)} - Exiting...\n")
        except FileNotFoundError as _:
            print(f"\nFile not found: {repr(_)} - Exiting...\n")
        except Exception as _:
            print(f"\nError: {repr(_)} - Exiting...\n")
    return wrapper

def get_datafeeds_and_statuses(service, merchant_id):
    datafeeds_info = {}
    # Fetch datafeeds
    request_datafeeds = service.datafeeds().list(merchantId=merchant_id)
    result_datafeeds = request_datafeeds.execute()
    datafeeds = result_datafeeds.get('resources') if result_datafeeds else []
    for datafeed in datafeeds:
        datafeeds_info[datafeed['id']] = {
            'name': datafeed['name'],
            'datafeedId': datafeed['id']
        }
    # Fetch datafeed statuses
    request_statuses = service.datafeedstatuses().list(merchantId=merchant_id)
    result_statuses = request_statuses.execute()
    statuses = result_statuses.get('resources') if result_statuses else []
    for status in statuses:
        datafeed_id = status['datafeedId']
        if datafeed_id in datafeeds_info:
            datafeeds_info[datafeed_id].update({
                'processingStatus': status.get('processingStatus'),
                'itemsValid': status.get('itemsValid'),
                'itemsTotal': status.get('itemsTotal')
            })

    return datafeeds_info

def process_datafeed_info(output_choice, prop_name, data, file_name):
    total_items_str = data.get('itemsTotal', 'N/A')
    valid_items_str = data.get('itemsValid', 'N/A')
    total_items = int(total_items_str) if total_items_str not in ('N/A', None) else 0
    valid_items = int(valid_items_str) if valid_items_str not in ('N/A', None) else 0
    item_errors = total_items - valid_items
    if output_choice == '1':
        if data['processingStatus'] != 'success' or item_errors > 0:
            print('Status: %s   | Property: %s  | Feed: %s / %s, with %s item errors' % (
                data['processingStatus'].upper() if 'processingStatus' in data else 'N/A',
                prop_name,
                data['name'] if 'name' in data else 'N/A',
                data['datafeedId'] if 'datafeedId' in data else 'N/A',
                item_errors if item_errors >= 0 else 'N/A'
            ))    
    elif output_choice == '2':
        if not file_name:
            # Generate timestamp for the default file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"feed-report-{timestamp}.csv"
            print("Parsing feed data and preparing to write to file...")

        row = [
            prop_name,
            data.get('name', 'N/A'),
            data.get('datafeedId', 'N/A'),
            data.get('processingStatus', 'N/A').upper(),
            str(item_errors) if item_errors >= 0 else 'N/A',
            str(valid_items) if 'itemsValid' in data else 'N/A',
            str(total_items) if 'itemsTotal' in data else 'N/A',
        ]
        path = os.getcwd()
        try:
            # Check if the file exists or create a new file with headers
            write_headers = not os.path.exists(file_name)
            with open(file_name, 'a', newline='', encoding='utf-8') as file:
                if write_headers:
                    header_row = ["Property", "Feed Name", "Feed ID", "Feed Status", "Item Errors", "Valid Items",
                                  "Total Items"]
                    file.write(','.join(header_row) + '\n')
                file.write(','.join(row) + '\n')
        except Exception as e:
            print(f"Error saving to file: {e}")
        else:
            if not file_name:
                print(f"Default file name: {file_name}")
                print(f"Saving output to {path}/{file_name}")

    elif output_choice == '3':
        print('Property: %s | Feed: %s / %s | Status: %s, with %s errors on %s of %s products.' % (
            prop_name,
            data['name'] if 'name' in data else 'N/A',
            data['datafeedId'] if 'datafeedId' in data else 'N/A',
            data['processingStatus'].upper() if 'processingStatus' in data else 'N/A',
            item_errors if item_errors >= 0 else 'N/A',
            data['itemsValid'] if 'itemsValid' in data else 'N/A',
            data['itemsTotal'] if 'itemsTotal' in data else 'N/A',
        ))
    else:
        print("Option choice invalid")
        sys.exit(1)

def main_menu(argv):
    print("\n---- Initializing Google Merchant Center Feed Status Report by JDT ----\n\n"
      "What report view would you like to see?\n"
      "1. Run a status check and report all failed feed fetch attempts and item errors\n"
      "2. Retrieve all properties feed data and save to csv file\n"
      "3. Output all feed data from all properties for review")
    output_choice = input("Enter your choice (1, 2, or 3): ")
    print("Configuring authorization and services...")

    # Authenticate and construct service.
    service, config, _ = _common.init(argv, __doc__)
    merchant_ids = _common.read_merchant_ids(config['config_path'] + '/merchant-info.json')

    # Get input for file name from the user only for Option 2
    if output_choice == '2':
        file_name = input("Enter desired file name now or leave empty for default (feed-report.csv): ").strip()
        if not file_name:
            # Generate timestamp for the default file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"feed-report-{timestamp}.csv"
        else:
            file_name = file_name + ".csv"
    else:
        # For Option 1 and Option 3, no need to prompt for a file name
        file_name = None

    path = os.getcwd()  # Define path here
    print("Analyzing feeds...")
    for merchant_info in merchant_ids:
        merchant_id = merchant_info['merchantId']
        prop_name = merchant_info['propName']
        combined_info = get_datafeeds_and_statuses(service, merchant_id)

        # Iterate over each data entry in the list
        for data_entry in list(combined_info.values()):
            process_datafeed_info(output_choice, prop_name, data_entry, file_name)

    # Print the saved output message only if Option 2 is selected
    if output_choice == '2' and path is not None:
        print(f"Saving output to {path}/{file_name}")
    print("Feed report complete!")

@handle_exceptions
def main(argv):
    main_menu(argv)

if __name__ == '__main__':
    main(sys.argv)
