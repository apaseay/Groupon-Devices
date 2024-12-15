
import pandas as pd
from datetime import datetime, timedelta

# Correct file path
file_path = "/Users/apase/Downloads/CSV folder/kandji.csv"
data = pd.read_csv(file_path)

# set cutoff date to 6 months ago
six_months_ago = datetime.now() - timedelta(days=6 * 30) # 180 days, roughly 6 months

#Convert 'Checked In' to datetime, handling erors
data['Checked In'] = pd.to_datetime(data['Checked In'], errors='coerce')

# Remove timezone information (make it naive)
data['Checked In'] = data['Checked In'].dt.tz_localize(None)

# Ensure six_months_ago is timezone naive (no timezone info)
six_months_ago = six_months_ago.replace(tzinfo=None)

# Filter devices that last checked in more than 6 months ago
outdated_devices = data[data['Checked In'] < six_months_ago]

# Show the result
print("Devices that last checked in more than 6 months ago:")
print(outdated_devices[['Device Name', 'Checked In']])
# Save the filtered to a new CSV file
outdated_devices.to_csv("outdated_devices.csv", index=False)