
import csv
import math

from software.config import FINGERPRINTS_FILE


def load_reference_fingerprints(path=FINGERPRINTS_FILE):
    with path.open("r", newline="") as file:
        return {
            row["Sample_ID"]: [
                float(row["R_G"]),
                float(row["B_G"]),
                float(row["R_B"]),
            ]
            for row in csv.DictReader(file)
        }


def calculate_distance(first, second):
    if len(first) != len(second):
        raise ValueError("Fingerprints must have the same number of features.")
    return math.sqrt(sum((left - right) ** 2 for left, right in zip(first, second)))


def find_closest_match(fingerprint, references):
    if not references:
        raise ValueError("At least one reference fingerprint is required.")
    return min(
        ((tag, calculate_distance(fingerprint, reference)) for tag, reference in references.items()),
        key=lambda match: match[1],
    )


def main():
    references = load_reference_fingerprints()
    unknown_fingerprint = [1.20, 0.80, 1.50]

    print("Q-SIGN FINGERPRINT MATCHING")
    print("============================")
    for tag, reference in references.items():
        print(tag, "Distance:", round(calculate_distance(unknown_fingerprint, reference), 4))

    closest_tag, distance = find_closest_match(unknown_fingerprint, references)
    print("\nClosest matching tag:", closest_tag)
    print("Matching distance:", round(distance, 4))


if __name__ == "__main__":
    main()
