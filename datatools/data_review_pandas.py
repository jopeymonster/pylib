# pandas
import pandas as pd

def review_data_pandas(df: pd.DataFrame, n_rows: int = 5) -> None:
    """
    Prints a summary of the DataFrame including:
    - First few rows
    - Data types
    - Missing value counts
    - Summary statistics for numeric columns
    - Unique value counts per column

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        n_rows (int, optional): Number of rows to display from the top. Defaults to 5.
    """
    print("Data Review:")
    print(df.head(n_rows))
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nSummary Statistics:")
    print(df.describe())
    print("\nUnique Values:")
    for column in df.columns:
        print(f"{column}: {df[column].nunique()} unique values")

def main():
    print("Pandas Data Review Tool - Supply a CSV file for review.")
    datafile = input("Enter the path to the CSV file: ")
    try:
        df = pd.read_csv(datafile)
        review_data_pandas(df)
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