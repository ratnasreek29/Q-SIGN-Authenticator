
import random
import csv
from pathlib import Path

READINGS_FILE = Path(__file__).resolve().parent / "readings.csv"

# Q-SIGN SENSOR SIMULATOR

# Base readings for our simulated tags
sample_data = {
    "TAG_A": {"R": 120, "G": 100, "B": 80, "C": 350},
    "TAG_B": {"R": 70, "G": 90, "B": 110, "C": 300},
    "TAG_C": {"R": 150, "G": 80, "B": 60, "C": 340}
}


# Function to generate one simulated scan
def simulate_scan(sample_id):

    base = sample_data[sample_id]

    red = base["R"] + random.randint(-3, 3)
    green = base["G"] + random.randint(-3, 3)
    blue = base["B"] + random.randint(-3, 3)
    clear = base["C"] + random.randint(-5, 5)

    readings = {
        "Sample_ID": sample_id,
        "Red": red,
        "Green": green,
        "Blue": blue,
        "Clear": clear
    }

    return readings


# Empty list to store all readings
all_readings = []


# Generate 10 scans for each tag
for tag in sample_data:

    print("\nGenerating data for", tag)

    for scan_number in range(1, 11):

        result = simulate_scan(tag)

        all_readings.append(result)

        print("Scan", scan_number, ":", result)


# Save readings into a CSV file
with READINGS_FILE.open("w", newline="") as file:

    fieldnames = ["Sample_ID", "Red", "Green", "Blue", "Clear"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(all_readings)


print("\nDataset successfully saved as readings.csv!")
print("Total number of readings:", len(all_readings))
