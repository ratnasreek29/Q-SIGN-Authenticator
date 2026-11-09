
import csv
from software.config import FINGERPRINTS_FILE, READINGS_FILE
from software.processing.preprocessing import extract_rgb_features

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
    try:
        red_green, blue_green, red_blue = extract_rgb_features(red, green, blue)
    except ValueError:
        continue

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



# Step 5: Save only NEW fingerprints without overwriting existing tags

fieldnames = ["Sample_ID", "R_G", "B_G", "R_B"]

# Load existing registered tag IDs
existing_tags = set()

if FINGERPRINTS_FILE.exists() and FINGERPRINTS_FILE.stat().st_size > 0:
    with FINGERPRINTS_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != fieldnames:
            raise ValueError(
                "Unexpected fingerprint CSV format. "
                "Existing data has not been modified."
            )

        existing_tags = {
            row["Sample_ID"].strip().upper()
            for row in reader
        }

# Identify fingerprints that are not already registered
new_fingerprints = [
    fingerprint
    for fingerprint in fingerprints
    if fingerprint["Sample_ID"].strip().upper() not in existing_tags
]

# Create the data directory if necessary
FINGERPRINTS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Append only new tags
if new_fingerprints:
    file_exists = (
        FINGERPRINTS_FILE.exists()
        and FINGERPRINTS_FILE.stat().st_size > 0
    )

    with FINGERPRINTS_FILE.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerows(new_fingerprints)

    print(f"\n{len(new_fingerprints)} new fingerprint(s) saved.")
else:
    print("\nNo new fingerprints to save.")

print("Existing registered fingerprints were preserved.")
