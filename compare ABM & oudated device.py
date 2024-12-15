import pandas as pd
import os

# Define file paths
file1_path = "/Users/apase/Downloads/CSV folder/Apple Business Manager.csv"
file2_path = "/Users/apase/Downloads/CSV folder/outdated_devices.csv"
output_file_path = "/Users/apase/Downloads/CSV folder/common_serials_filtered.csv"

# Check if files exist
if not os.path.exists(file1_path) or not os.path.exists(file2_path):
    print("One or both file paths do not exist.")
    exit()

# Attempt to load the CSV files with a fallback for encoding errors
try:
    data1 = pd.read_csv(file1_path, encoding='utf-8')  # Default encoding
except UnicodeDecodeError:
    print(f"Error reading {file1_path} with 'utf-8'. Trying 'latin1'.")
    data1 = pd.read_csv(file1_path, encoding='latin1')

try:
    data2 = pd.read_csv(file2_path, encoding='utf-8')  # Default encoding
except UnicodeDecodeError:
    print(f"Error reading {file2_path} with 'utf-8'. Trying 'latin1'.")
    data2 = pd.read_csv(file2_path, encoding='latin1')

# Normalize column names
data1.columns = data1.columns.str.strip().str.upper()
data2.columns = data2.columns.str.strip().str.upper()

# Check for the 'SERIAL_NO' column
if 'SERIAL_NO' not in data1.columns or 'SERIAL_NO' not in data2.columns:
    print("One of the files is missing the 'SERIAL_NO' column.")
    exit()

# Drop rows with missing SERIAL_NO values
data1 = data1.dropna(subset=['SERIAL_NO'])
data2 = data2.dropna(subset=['SERIAL_NO'])

# Extract unique serial numbers
serials1 = set(data1['SERIAL_NO'])
serials2 = set(data2['SERIAL_NO'])

# Find common serial numbers
common_serials = serials1.intersection(serials2)

# Print results
print(f"Found {len(common_serials)} common serial numbers.")
if not common_serials:
    print("No common serial numbers found.")
    exit()

# Filter rows in data1 based on common serials
filtered_data = data1[data1['SERIAL_NO'].isin(common_serials)]

# Save the filtered data
try:
    filtered_data.to_csv(output_file_path, index=False)
    print(f"Filtered data saved to: {output_file_path}")
except Exception as e:
    print(f"Error saving the file: {e}")
