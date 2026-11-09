
import csv

from software.config import FINGERPRINTS_FILE
from software.processing.preprocessing import extract_rgb_features


def register_tag(tag_id, red, green, blue, path=FINGERPRINTS_FILE):
    tag_id = tag_id.strip().upper()

    if not tag_id:
        raise ValueError("Tag ID cannot be empty.")

    rgb_values = (red, green, blue)

    if any(
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < 0
        or value > 255
        for value in rgb_values
    ):
        raise ValueError("RGB values must be whole numbers from 0 to 255.")

    if green == 0 or blue == 0:
        raise ValueError("Green and Blue must be greater than zero.")

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["Sample_ID", "R_G", "B_G", "R_B"]
    existing_tags = set()

    if path.exists() and path.stat().st_size > 0:
        with path.open("r", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != fieldnames:
                raise ValueError(
                    "Unexpected fingerprint CSV format. "
                    "Check the file before registering a tag."
                )

            existing_tags = {
                row["Sample_ID"].strip().upper()
                for row in reader
            }

    if tag_id in existing_tags:
        raise ValueError(f"Tag {tag_id} is already registered.")

    r_g, b_g, r_b = extract_rgb_features(red, green, blue)

    fingerprint = {
        "Sample_ID": tag_id,
        "R_G": round(r_g, 4),
        "B_G": round(b_g, 4),
        "R_B": round(r_b, 4),
    }

    file_exists = path.exists() and path.stat().st_size > 0

    with path.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(fingerprint)

    return fingerprint


def main():
    print("Q-SIGN TAG REGISTRATION")
    print("=======================")

    try:
        tag_id = input("Enter new Tag ID: ")
        red = int(input("Enter Red (0-255): "))
        green = int(input("Enter Green (0-255): "))
        blue = int(input("Enter Blue (0-255): "))

        fingerprint = register_tag(tag_id, red, green, blue)

        print("\nTag registered successfully!")
        print("Tag ID:", fingerprint["Sample_ID"])
        print("R/G:", fingerprint["R_G"])
        print("B/G:", fingerprint["B_G"])
        print("R/B:", fingerprint["R_B"])

    except ValueError as error:
        print("\nRegistration failed:", error)


if __name__ == "__main__":
    main()
