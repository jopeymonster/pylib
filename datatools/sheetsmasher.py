import pandas as pd
import os
from datetime import datetime

# var declaration
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def menu():
    print("\nCSV to Excel XSLX Sheet Smasher\n"
          "Provide multiple CSV files and combine them into 1 XSLX.\n")
    csv_files = input("Enter CSV file paths separated by commas: ").split(",")
    filename = input(f"Enter a new workbook file name (if left blank, default name will be 'combined-{timestamp}.xlsx'): ").strip()
    filename = f"{filename}-{timestamp}.xlsx" if filename else f"combined-{timestamp}.xlsx"  # Default if blank    
    csvs_to_excel(csv_files, filename)

def sanitize_sheet_name(name):
    """Ensure sheet names are Excel-compatible."""
    invalid_chars = '[]:*?/\\'
    for ch in invalid_chars:
        name = name.replace(ch, "")
    return name[:31]  # Excel sheet names max length is 31 characters

def csvs_to_excel(csv_files, filename):
    """
    Combines multiple CSV files into one Excel workbook.

    Each CSV is placed in a separate sheet, named after the file (truncated to 31 characters).
    
    :param csv_files: List of CSV file paths.
    :param filename: Name of the output Excel file.
    """
    # Ensure file extension is .xlsx
    if not filename.lower().endswith(".xlsx"):
        filename += ".xlsx"
    # Create an Excel writer object outside the loop
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for file in csv_files:
                file = file.strip()  # Clean whitespace
                if not os.path.isfile(file):  
                    print(f"Warning: {file} does not exist. Skipping.")
                    continue
                try:
                    df = pd.read_csv(file)
                    sheet_name = sanitize_sheet_name(os.path.basename(file))
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"Added {file} as sheet '{sheet_name}'")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
            print(f"Excel workbook saved as '{filename}'")
    except Exception as e:
        print(f"Error creating Excel file: {e}")

def main() -> None:
    menu()

if __name__ == '__main__':
    main()
