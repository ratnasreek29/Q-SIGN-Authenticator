
import csv
from pathlib import Path

READINGS_FILE = Path(__file__).resolve().parent / "readings.csv"

# Open the dataset
with READINGS_FILE.open("r", newline="") as file:

    reader = csv.DictReader(file)

    print("Q-SIGN DATASET")
    print("-------------------------")

    # Display every reading
    for row in reader:
        print(row)
