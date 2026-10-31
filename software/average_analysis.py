
import csv
from pathlib import Path

READINGS_FILE = Path(__file__).resolve().parent / "readings.csv"

# Create an empty dictionary to store readings
tag_readings = {}

# Open the CSV dataset
with READINGS_FILE.open("r", newline="") as file:

    reader = csv.DictReader(file)

    # Read every row
    for row in reader:

        tag = row["Sample_ID"]

        # Create an empty list for a new tag
        if tag not in tag_readings:
            tag_readings[tag] = {
                "Red": [],
                "Green": [],
                "Blue": [],
                "Clear": []
            }

        # Store the sensor readings
        tag_readings[tag]["Red"].append(int(row["Red"]))
        tag_readings[tag]["Green"].append(int(row["Green"]))
        tag_readings[tag]["Blue"].append(int(row["Blue"]))
        tag_readings[tag]["Clear"].append(int(row["Clear"]))


# Calculate and display averages
print("Q-SIGN AVERAGE SENSOR READINGS")
print("================================")

for tag, readings in tag_readings.items():

    print("\nTag:", tag)

    for colour, values in readings.items():

        average = sum(values) / len(values)

        print("Average", colour, ":", round(average, 2))
