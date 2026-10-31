
import csv
from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parent
READINGS_FILE = SOFTWARE_DIR / "readings.csv"
FINGERPRINTS_FILE = SOFTWARE_DIR / "fingerprints.csv"

tag_readings = {}

# Step 1: Read the sensor dataset
with READINGS_FILE.open("r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        tag = row["Sample_ID"]

        if tag not in tag_readings:
            tag_readings[tag] = {
                "Red": [],
                "Green": [],
                "Blue": []
            }

        tag_readings[tag]["Red"].append(int(row["Red"]))
        tag_readings[tag]["Green"].append(int(row["Green"]))
        tag_readings[tag]["Blue"].append(int(row["Blue"]))


# Step 2: Calculate average RGB values
fingerprints = []

for tag, readings in tag_readings.items():

    red = sum(readings["Red"]) / len(readings["Red"])
    green = sum(readings["Green"]) / len(readings["Green"])
    blue = sum(readings["Blue"]) / len(readings["Blue"])

    # Step 3: Extract features
    if green != 0 and blue != 0:

        red_green = red / green
        blue_green = blue / green
        red_blue = red / blue

        fingerprints.append({
            "Sample_ID": tag,
            "R_G": round(red_green, 4),
            "B_G": round(blue_green, 4),
            "R_B": round(red_blue, 4)
        })


# Step 4: Display the fingerprints
print("Q-SIGN OPTICAL FINGERPRINTS")
print("============================")

for fingerprint in fingerprints:
    print(fingerprint)


# Step 5: Save fingerprints into a CSV file
with FINGERPRINTS_FILE.open("w", newline="") as file:

    fieldnames = ["Sample_ID", "R_G", "B_G", "R_B"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(fingerprints)

print("\nFingerprints successfully saved!")
