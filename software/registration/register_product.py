
import csv
from software.config import FINGERPRINTS_FILE
from software.database.product_registry import register_product


def main():
    with FINGERPRINTS_FILE.open("r", newline="") as file:
        available_tags = [row["Sample_ID"] for row in csv.DictReader(file)]

    product_id = input("Enter new Product ID: ").strip().upper()
    print("\nAvailable optical tags:")
    for tag in available_tags:
        print("-", tag)
    selected_tag = input("\nEnter optical tag: ").strip().upper()

    if selected_tag not in available_tags:
        print("Invalid optical tag.")
        return

    try:
        product_id, selected_tag = register_product(product_id, selected_tag)
    except ValueError as error:
        print(error)
        return

    print("\nProduct registered successfully!")
    print("Product ID:", product_id)
    print("Optical Tag:", selected_tag)


if __name__ == "__main__":
    main()
