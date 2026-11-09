
from software.acquisition.manual_input import read_rgb_reading
from software.authentication.fingerprint_matching import (
    calculate_distance,
    load_reference_fingerprints,
)
from software.config import MATCH_THRESHOLD
from software.database.product_registry import load_product_registry
from software.processing.preprocessing import extract_rgb_features


def authenticate_reading(product_id, rgb_reading, products, references, threshold=MATCH_THRESHOLD):
    if product_id not in products:
        raise KeyError(f"Product {product_id} is not registered.")

    expected_tag = products[product_id]
    if expected_tag not in references:
        raise KeyError(f"No reference fingerprint exists for {expected_tag}.")

    fingerprint = extract_rgb_features(*rgb_reading)
    distance = calculate_distance(fingerprint, references[expected_tag])
    return expected_tag, distance, distance <= threshold


def main():
    products = load_product_registry()
    references = load_reference_fingerprints()

    print("Q-SIGN PRODUCT AUTHENTICATION")
    print("==============================")
    product_id = input("Enter Product ID: ").strip().upper()
    try:
        expected_tag, distance, matched = authenticate_reading(
            product_id, read_rgb_reading(), products, references
        )
    except KeyError as error:
        print("\n", error.args[0])
        return
    except ValueError as error:
        print("\nINVALID SENSOR READINGS:", error)
        return

    print("\nRegistered product:", product_id)
    print("Expected optical tag:", expected_tag)
    print("Distance:", round(distance, 4))
    print("\nPOSSIBLE MATCH" if matched else "\nFINGERPRINT MISMATCH")


if __name__ == "__main__":
    main()
