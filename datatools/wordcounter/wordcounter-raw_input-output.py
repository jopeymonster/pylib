# querycounter-raw_input-output.py

# Request user input for the list of queries
input_queries = input("Enter the list of queries, separated by commas: ")
strings = [s.strip() for s in input_queries.split(',')]

# Create a array to store word frequencies
word_frequency = {}

# Count the occurrences of each word
total_words = 0
for string in strings:
    words = string.split()
    total_words += len(words)
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1

# Calculate the frequency of each unique word
word_percentage = {}
for word, frequency in word_frequency.items():
    word_percentage[word] = frequency / total_words

# Print results
print("\nUnique Words and Their Frequencies:")
for word, frequency in word_frequency.items():
    print(f"{word}: {frequency}")

print("\nWord Frequencies as a Percentage of Total Words:")
for word, percentage in word_percentage.items():
    print(f"{word}: {percentage:.2%}")