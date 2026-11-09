
import csv
import math
from software.config import READINGS_FILE

# Step 1: Read all sensor readings
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

            features = [
                red / green,
                blue / green,
                red / blue
            ]

            tag_data[tag].append(features)


# Step 2: Divide readings into groups
reference_data = {}
calibration_data = {}
test_data = {}

for tag, readings in tag_data.items():

    reference_data[tag] = readings[:6]
    calibration_data[tag] = readings[6:8]
    test_data[tag] = readings[8:10]


# Step 3: Calculate average reference fingerprints
reference_database = {}

for tag, readings in reference_data.items():

    averages = []

    for feature_index in range(3):

        values = [reading[feature_index] for reading in readings]

        averages.append(sum(values) / len(values))

    reference_database[tag] = averages


# Step 4: Create distance calculation function
def calculate_distance(first, second):

    total = 0

    for i in range(3):

        total += (first[i] - second[i]) ** 2

    return math.sqrt(total)


# Step 5: Find closest reference for a reading
def find_closest_tag(reading):

    distances = {}

    for tag, reference in reference_database.items():

        distances[tag] = calculate_distance(reading, reference)

    closest_tag = min(distances, key=distances.get)

    return closest_tag, distances[closest_tag]


# Step 6: Calibrate the threshold
calibration_distances = []

for tag, readings in calibration_data.items():

    for reading in readings:

        predicted_tag, distance = find_closest_tag(reading)

        calibration_distances.append(distance)

threshold = max(calibration_distances) * 1.2

print("CALIBRATED THRESHOLD:", round(threshold, 6))


# Step 7: Test the system
correct = 0
unknown = 0
total = 0

print("\nQ-SIGN PERFORMANCE EVALUATION")
print("==============================")

for actual_tag, readings in test_data.items():

    for reading in readings:

        predicted_tag, distance = find_closest_tag(reading)

        total += 1

        if distance > threshold:

            result = "UNKNOWN"
            unknown += 1

        else:

            result = predicted_tag

            if predicted_tag == actual_tag:
                correct += 1

        print(
            "Actual:", actual_tag,
            "| Predicted:", result,
            "| Distance:", round(distance, 6)
        )


# Step 8: Display results
accuracy = (correct / total) * 100

print("\nEVALUATION SUMMARY")
print("==================")
print("Total test readings:", total)
print("Correct identifications:", correct)
print("Unknown classifications:", unknown)
print("Identification accuracy:", round(accuracy, 2), "%")
