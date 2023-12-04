import csv
import json

# Sample JSON data
json_data = [
    {"Name": "Alice", "Age": 25, "City": "New York"},
    {"Name": "Bob", "Age": 30, "City": "San Francisco"},
    {"Name": "Charlie", "Age": 35, "City": "Seattle"}
]

# Define the CSV file name
csv_file = 'output.csv'

# Write JSON data to CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=json_data[0].keys())
    
    # Write header
    writer.writeheader()
    
    # Write JSON data as rows in CSV
    writer.writerows(json_data)

print(f"JSON data has been written to '{csv_file}' as a CSV file.")
