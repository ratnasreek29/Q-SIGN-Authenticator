
import csv
import math
from pathlib import Path

FINGERPRINTS_FILE = Path(__file__).resolve().parent / "fingerprints.csv"

# STEP 1: Create product-to-tag mapping

product_database = {
    "PROD_001": "TAG_A",
    "PROD_002": "TAG_B",
    "PROD_003": "TAG_C"
}


# STEP 2: Load registered fingerprints

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


# STEP 3: Get product ID

print("Q-SIGN PRODUCT AUTHENTICATION")
print("==============================")

product_id = input("Enter Product ID: ").strip().upper()


# STEP 4: Check whether product is registered

if product_id not in product_database:

    print("\nPRODUCT NOT REGISTERED")

else:

    expected_tag = product_database[product_id]

    print("\nRegistered product:", product_id)
    print("Expected optical tag:", expected_tag)


    # STEP 5: Enter new sensor readings

    red = float(input("Enter Red value: "))
    green = float(input("Enter Green value: "))
    blue = float(input("Enter Blue value: "))


    if green == 0 or blue == 0:

        print("\nINVALID SENSOR READINGS")

    else:

        # STEP 6: Extract fingerprint features

        unknown_fingerprint = [
            red / green,
            blue / green,
            red / blue
        ]


        # STEP 7: Retrieve expected fingerprint

        expected_fingerprint = reference_database[expected_tag]


        # STEP 8: Calculate Euclidean distance

        total = 0

        for i in range(3):

            difference = (
                unknown_fingerprint[i] -
                expected_fingerprint[i]
            )

            total += difference ** 2

        distance = math.sqrt(total)


        # STEP 9: Apply provisional threshold

        threshold = 0.10

        print("\nAUTHENTICATION RESULTS")
        print("======================")

        print("Expected fingerprint:", expected_fingerprint)
        print("Scanned fingerprint:", unknown_fingerprint)
        print("Distance:", round(distance, 4))

        if distance <= threshold:

            print("\nPOSSIBLE MATCH")

        else:

            print("\nFINGERPRINT MISMATCH")
