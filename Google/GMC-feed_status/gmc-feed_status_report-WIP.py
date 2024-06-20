# gmc-feed_status_update

# imports
from __future__ import print_function
import sys
import os
import csv
from datetime import datetime
import requests
from tabulate import tabulate
import googleapiclient.errors
from content import _common

# exceptions
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except googleapiclient.errors.HttpError as e:
            print_error(func.__name__, e)   
        except requests.exceptions.RequestException as e:
            print_error(func.__name__, e)
        except ValueError as e:
            print_error(func.__name__, e)
        except KeyboardInterrupt as e:
            print_error(func.__name__, e)
        except FileNotFoundError as e:
            print_error(func.__name__, e)
        except AttributeError as e:
            print_error(func.__name__, e)
        except Exception as e:
            print_error(func.__name__, e)
            
    def print_error(func_name, error):
        print(f"\nError in function '{func_name}': {repr(error)} - Exiting...\n")
        
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
    
    # Accumulate data for each property
    all_data = []
    for merchant_info in merchant_ids:
        merchant_id = merchant_info['merchantId']
        prop_name = merchant_info['propName']
        combined_info = get_datafeeds_and_statuses(service, merchant_id)

        # Iterate over each data entry in the list
        for data_entry in list(combined_info.values()):
            total_items_str = data_entry.get('itemsTotal', 'N/A')
            valid_items_str = data_entry.get('itemsValid', 'N/A')
            total_items = int(total_items_str) if total_items_str not in ('N/A', None) else 0
            valid_items = int(valid_items_str) if valid_items_str not in ('N/A', None) else 0
            item_errors = total_items - valid_items
            
            if output_choice == '1':
                if data_entry['processingStatus'] != 'success' or item_errors > 0:
                    all_data.append([prop_name, data_entry.get('name', 'N/A'), data_entry.get('datafeedId', 'N/A'),
                                     data_entry.get('processingStatus', 'N/A').upper(),
                                     item_errors if item_errors >= 0 else 'N/A'])
                   
            elif output_choice == '2':
                row = [
                    prop_name,
                    data_entry.get('name', 'N/A'),
                    data_entry.get('datafeedId', 'N/A'),
                    data_entry.get('processingStatus', 'N/A').upper(),
                    str(item_errors) if item_errors >= 0 else 'N/A',
                    str(valid_items) if 'itemsValid' in data_entry else 'N/A',
                    str(total_items) if 'itemsTotal' in data_entry else 'N/A',
                ]
                all_data.append(row)

            elif output_choice == '3':
                all_data.append([prop_name, 
                                 data_entry.get('name', 'N/A'), 
                                 data_entry.get('datafeedId', 'N/A'),
                                 data_entry.get('processingStatus', 'N/A').upper(),
                                 item_errors if item_errors >= 0 else 'N/A',
                                 data_entry.get('itemsValid', 'N/A'),
                                 data_entry.get('itemsTotal', 'N/A')])

            else:
                print("Option choice invalid")
                sys.exit(1)

    # Print the tabulate table for all accumulated data
    if all_data:
        headers = ["Property", "Feed Name", "Feed ID", "Status", "Item Errors"]
        if output_choice in ['2','3']:
            headers += ["Valid Items", "Total Items"]
        print(tabulate(all_data, headers=headers, tablefmt="simple_grid"))
        
        # Save to file if Option 2 is selected
        if output_choice == '2' and path is not None:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(all_data)
                print(f"Saving output to {path}/{file_name}")
            except Exception as e:
                print(f"Error saving to file: {e}")
    else:
        print("No data to display!")

    print("\nFeed report complete!")

# automated function for use in future builds
# def auto_menu(argv):
#     print("\n---- Initializing Google Merchant Center Feed Status Report by JDT ----\n\n"
#           "---- Automated ----\n")
#     sys.exit("Automated menu reached")

@handle_exceptions
def main(argv):
    main_menu(argv)

if __name__ == '__main__':
    main(sys.argv)
