import os

# List all system and environment variables
for key, value in os.environ.items():
    print(f"{key} = {value}")
