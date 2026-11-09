
import csv
from software.config import FINGERPRINTS_FILE

# Create an empty reference database
reference_database = {}

# Read the extracted fingerprints
with FINGERPRINTS_FILE.open("r", newline="") as file:

    reader = csv.DictReader(file)

    for row in reader:

        tag = row["Sample_ID"]

        reference_database[tag] = {
            "R_G": float(row["R_G"]),
            "B_G": float(row["B_G"]),
            "R_B": float(row["R_B"])
        }


# Display the reference database
print("Q-SIGN REFERENCE DATABASE")
print("==========================")

for tag, fingerprint in reference_database.items():

    print("\nTag:", tag)
    print("R/G:", fingerprint["R_G"])
    print("B/G:", fingerprint["B_G"])
    print("R/B:", fingerprint["R_B"])


print("\nReference database loaded successfully!")
