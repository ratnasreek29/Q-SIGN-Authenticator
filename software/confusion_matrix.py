
import csv
import math
from pathlib import Path

READINGS_FILE = Path(__file__).resolve().parent / "readings.csv"

# Step 1: Read sensor readings
tag_data = {}

with READINGS_FILE.open("r", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        tag = row["Sample_ID"]

        if tag not in tag_data:
            tag_data[tag] = []

        red = int(row["Red"])
        green = int(row["Green"])
        blue = int(row["Blue"])

        if green != 0 and blue != 0:

            tag_data[tag].append([
                red / green,
                blue / green,
                red / blue
            ])


# Step 2: Split the dataset
reference_data = {}
calibration_data = {}
test_data = {}

for tag, readings in tag_data.items():

    reference_data[tag] = readings[:6]
    calibration_data[tag] = readings[6:8]
    test_data[tag] = readings[8:10]


# Step 3: Build reference fingerprints
reference_database = {}

for tag, readings in reference_data.items():

    reference_database[tag] = [
        sum(reading[i] for reading in readings) / len(readings)
        for i in range(3)
    ]


# Step 4: Calculate distance
def calculate_distance(first, second):

    total = 0

    for i in range(3):
        total += (first[i] - second[i]) ** 2

    return math.sqrt(total)


# Step 5: Find closest tag
def find_closest_tag(reading):

    distances = {}

    for tag, reference in reference_database.items():

        distances[tag] = calculate_distance(reading, reference)

    closest_tag = min(distances, key=distances.get)

    return closest_tag, distances[closest_tag]


# Step 6: Calibrate threshold
calibration_distances = []

for readings in calibration_data.values():

    for reading in readings:

        _, distance = find_closest_tag(reading)
        calibration_distances.append(distance)

threshold = max(calibration_distances) * 1.2


# Step 7: Create confusion matrix
tags = list(reference_database.keys())

predicted_labels = tags + ["UNKNOWN"]

matrix = {
    actual: {predicted: 0 for predicted in predicted_labels}
    for actual in tags
}

for actual_tag, readings in test_data.items():

    for reading in readings:

        predicted_tag, distance = find_closest_tag(reading)

        if distance > threshold:
            predicted_tag = "UNKNOWN"

        matrix[actual_tag][predicted_tag] += 1


# Step 8: Display confusion matrix
print("Q-SIGN CONFUSION MATRIX")
print("========================")

print("Actual / Predicted", *predicted_labels, sep="\t")

for actual_tag in tags:

    print(
        actual_tag,
        *[matrix[actual_tag][predicted] for predicted in predicted_labels],
        sep="\t"
    )


# Step 9: Calculate correct identification rate
total = 0
correct = 0

for actual_tag in tags:

    for predicted_tag in predicted_labels:

        count = matrix[actual_tag][predicted_tag]
        total += count

        if actual_tag == predicted_tag:
            correct += count

accuracy = (correct / total) * 100 if total else 0

print("\nPERFORMANCE REPORT")
print("==================")
print("Total test readings:", total)
print("Correct identifications:", correct)
print("Incorrect or unknown results:", total - correct)
print("Identification accuracy:", round(accuracy, 2), "%")
print("Threshold:", round(threshold, 6))
