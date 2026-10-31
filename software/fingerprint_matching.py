
import csv
import math
from pathlib import Path

FINGERPRINTS_FILE = Path(__file__).resolve().parent / "fingerprints.csv"

# Step 1: Load the reference database
reference_database = {}

with FINGERPRINTS_FILE.open("r", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        tag = row["Sample_ID"]

        reference_database[tag] = [
            float(row["R_G"]),
            float(row["B_G"]),
            float(row["R_B"])
        ]


# Step 2: Enter an unknown fingerprint
# These are simulated test values for now.

unknown_fingerprint = [1.20, 0.80, 1.50]


# Step 3: Calculate Euclidean distance
def calculate_distance(fingerprint1, fingerprint2):

    total = 0

    for i in range(len(fingerprint1)):

        difference = fingerprint1[i] - fingerprint2[i]

        total += difference ** 2

    distance = math.sqrt(total)

    return distance


# Step 4: Compare with every reference tag
print("Q-SIGN FINGERPRINT MATCHING")
print("============================")

distances = {}

for tag, reference in reference_database.items():

    distance = calculate_distance(
        unknown_fingerprint,
        reference
    )

    distances[tag] = distance

    print(tag, "Distance:", round(distance, 4))


# Step 5: Find the closest candidate
closest_tag = min(distances, key=distances.get)

print("\nClosest matching tag:", closest_tag)
print("Matching distance:", round(distances[closest_tag], 4))
