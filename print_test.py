# Import modules for basic functionality
import os
import sys
import time
from datetime import datetime

# Function to write to both console and file
def log_message(message):
    # Print to console
    print(message, flush=True)
    # Write to file
    with open('output.txt', 'a') as f:
        f.write(message + '\n')

# Start logging
log_message("=== Starting Test ===")
log_message(f"Current time: {datetime.now()}")
log_message(f"Python version: {sys.version}")
log_message(f"Current directory: {os.getcwd()}")

# List all files in directory
log_message("\nFiles in directory:")
for file in os.listdir():
    log_message(f"- {file}")

# Test some basic operations
log_message("\nTesting basic operations:")
for i in range(5):
    log_message(f"Operation {i+1}")
    time.sleep(1)  # Wait 1 second between operations

log_message("\n=== Test Complete ===")
