
import csv
import math
from software.config import FINGERPRINTS_FILE, MATCH_THRESHOLD

# Step 1: Load reference fingerprints
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
unknown_fingerprint = [1.20, 0.80, 1.50]


# Step 3: Set a provisional threshold
threshold = MATCH_THRESHOLD


# Step 4: Calculate Euclidean distance
def calculate_distance(fingerprint1, fingerprint2):

    total = 0

    for i in range(len(fingerprint1)):

        difference = fingerprint1[i] - fingerprint2[i]

        total += difference ** 2

    return math.sqrt(total)


# Step 5: Compare fingerprints
distances = {}

print("Q-SIGN AUTHENTICATION SYSTEM")
print("============================")

for tag, reference in reference_database.items():

    distance = calculate_distance(
        unknown_fingerprint,
        reference
    )

    distances[tag] = distance

    print(tag, "Distance:", round(distance, 4))


# Step 6: Find the closest reference
closest_tag = min(distances, key=distances.get)

minimum_distance = distances[closest_tag]

print("\nClosest candidate:", closest_tag)
print("Minimum distance:", round(minimum_distance, 4))


# Step 7: Apply threshold
print("\nAUTHENTICATION RESULT")

if minimum_distance <= threshold:

    print("POSSIBLE MATCH:", closest_tag)

else:

    print("UNKNOWN TAG")

print("\nThreshold used:", threshold)
