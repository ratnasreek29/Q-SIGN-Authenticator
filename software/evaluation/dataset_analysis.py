
import csv
from software.config import READINGS_FILE

# Open the dataset
with READINGS_FILE.open("r", newline="") as file:

    reader = csv.DictReader(file)

    print("Q-SIGN DATASET")
    print("-------------------------")

    # Display every reading
    for row in reader:
        print(row)
