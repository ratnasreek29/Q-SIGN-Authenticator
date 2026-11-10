
import csv
import math

from software.config import FINGERPRINTS_FILE


def load_reference_fingerprints(path=FINGERPRINTS_FILE):
    """
    Load registered optical fingerprints.

    Returns an empty dictionary if the fingerprint
    CSV does not exist or is empty.
    """

    # Handle a fresh Streamlit Cloud deployment.
    if not path.exists() or path.stat().st_size == 0:
        return {}

    fingerprints = {}

    with path.open("r", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "Sample_ID",
            "R_G",
            "B_G",
            "R_B",
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "Invalid fingerprint CSV format. "
                "Required columns: Sample_ID, R_G, B_G, R_B."
            )

        for row in reader:
            tag_id = row["Sample_ID"].strip().upper()

            if not tag_id:
                continue

            fingerprints[tag_id] = (
                float(row["R_G"]),
                float(row["B_G"]),
                float(row["R_B"]),
            )

    return fingerprints


def calculate_distance(features1, features2):
    """
    Calculate Euclidean distance between two
    normalized optical fingerprint vectors.
    """

    if len(features1) != len(features2):
        raise ValueError(
            "Fingerprint feature vectors must have equal lengths."
        )

    if len(features1) != 3:
        raise ValueError(
            "Each fingerprint must contain exactly three features."
        )

    return math.sqrt(
        sum(
            (float(a) - float(b)) ** 2
            for a, b in zip(features1, features2)
        )
    )
