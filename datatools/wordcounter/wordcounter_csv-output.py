# querycounter_csv-output-mk1.py

# imports
import csv
from datetime import datetime
import time

# prompt user for input file location
print("Query Parser by JDT.\nThis script will require a text or csv file with a list of queries.")
input_file = input("Enter the file location path: ")

# ingest data from file
try:
    with open(input_file, 'r') as file:
        strings = file.read().splitlines()
except FileNotFoundError:
    print("File not found.")
    exit()

# start time
start_time = time.time()

# create an array to store word frequencies
word_frequency = {}

# count the occurrences of each word
total_words = 0
for string in strings:
    words = string.split()
    total_words += len(words)
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1

# time outputend_time = time.time()
end_time = time.time()
execution_time = end_time - start_time

# calculate the frequency of each unique word
word_percentage = {}
for word, frequency in word_frequency.items():
    word_percentage[word] = frequency / total_words

# transform data for csv
output_data = [["Word", "Frequency", "Percentage"]]
for word, frequency in word_frequency.items():
    percentage = word_percentage[word]
    output_data.append([word, frequency, f"{percentage:.2%}"])

# create file with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
output_filename = f"query_counter_output-{timestamp}.csv"

# output file path
output_path = '/Users/joet/' + output_filename  

# write to CSV file
try:
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_data)
    print(f"Time taken for word frequency counting: {execution_time} seconds")
    print(f"The file has been processed.\nOutput file saved to {output_path}")
except IOError:
    print("Error writing to the output file.")
