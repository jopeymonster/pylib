import pandas as pd
import xarray as xr
import numpy as np

def review_data_xarray(data: xr.Dataset, sample_size: int = 5):
    """
    Review an xarray Dataset for key data quality and structural aspects.

    Parameters:
        data (xr.Dataset): The xarray Dataset to inspect.
        sample_size (int): Number of samples to show from each variable.
    """
    print("XArray Data Review:")
    
    # Display the dataset structure
    print("\nDataset Structure:")
    print(data.as_dataset())

def main():
    print("XArrary Data Review Tool - Supply a CSV file for review.")
    datafile = input("Enter the path to the CSV file: ")
    try:
        df = pd.read_csv(datafile)
        ds = df.to_xarray()
        review_data_xarray(ds)
    except FileNotFoundError:
        print(f"File {datafile} not found. Please check the path and try again.")
    except pd.errors.EmptyDataError:
        print(f"The file {datafile} is empty. Please provide a valid CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


"""
Colab usage:
try:
    # assuming 'data' file input above
    review_data(data)
except FileNotFoundError:
      print(f"{data} not found.")
except pd.errors.EmptyDataError:
      print(f"{data} is empty.")
except Exception as e:
      print(f"An error occurred: {e}")
"""