
import csv
import os
import tempfile

from software.config import FINGERPRINTS_FILE
from software.database.product_registry import load_product_registry
from software.processing.preprocessing import extract_rgb_features


FIELDNAMES = ["Sample_ID", "R_G", "B_G", "R_B"]


def load_tags(path=FINGERPRINTS_FILE):
    if not path.exists():
        return []

    with path.open("r", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != FIELDNAMES:
            raise ValueError("Unexpected fingerprint CSV format.")

        return list(reader)


def save_tags(tags, path=FINGERPRINTS_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to a temporary file first to reduce the risk
    # of damaging the original CSV during saving.
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            delete=False,
            dir=path.parent,
            suffix=".csv",
        ) as file:
            temporary_path = file.name
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(tags)

        os.replace(temporary_path, path)

    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)


def edit_tag(tag_id, red, green, blue):
    tag_id = tag_id.strip().upper()

    if not tag_id:
        raise ValueError("Tag ID cannot be empty.")

    values = (red, green, blue)

    if any(
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 0 <= value <= 255
        for value in values
    ):
        raise ValueError("RGB values must be integers from 0 to 255.")

    if green == 0 or blue == 0:
        raise ValueError("Green and Blue must be greater than zero.")

    tags = load_tags()

    selected_tag = next(
        (tag for tag in tags if tag["Sample_ID"].upper() == tag_id),
        None,
    )

    if selected_tag is None:
        raise ValueError(f"Tag {tag_id} does not exist.")

    r_g, b_g, r_b = extract_rgb_features(red, green, blue)

    selected_tag["R_G"] = round(r_g, 4)
    selected_tag["B_G"] = round(b_g, 4)
    selected_tag["R_B"] = round(r_b, 4)

    save_tags(tags)

    return selected_tag


def delete_tag(tag_id):
    tag_id = tag_id.strip().upper()

    if not tag_id:
        raise ValueError("Tag ID cannot be empty.")

    tags = load_tags()

    if not any(tag["Sample_ID"].upper() == tag_id for tag in tags):
        raise ValueError(f"Tag {tag_id} does not exist.")

    products = load_product_registry()

    linked_products = [
        product_id
        for product_id, assigned_tag in products.items()
        if assigned_tag.upper() == tag_id
    ]

    if linked_products:
        raise ValueError(
            f"Cannot delete {tag_id}. "
            f"It is assigned to: {', '.join(linked_products)}"
        )

    remaining_tags = [
        tag for tag in tags
        if tag["Sample_ID"].upper() != tag_id
    ]

    save_tags(remaining_tags)

    return tag_id


def main():
    print("\nQ-SIGN TAG MANAGEMENT")
    print("=====================")

    print("1. View registered tags")
    print("2. Edit tag")
    print("3. Delete tag")

    choice = input("\nSelect an option: ").strip()

    try:
        if choice == "1":
            tags = load_tags()

            if not tags:
                print("No tags registered.")

            for tag in tags:
                print(tag)

        elif choice == "2":
            tag_id = input("Enter Tag ID to edit: ")
            red = int(input("New Red: "))
            green = int(input("New Green: "))
            blue = int(input("New Blue: "))

            updated = edit_tag(tag_id, red, green, blue)

            print("\nTag updated successfully!")
            print(updated)

        elif choice == "3":
            tag_id = input("Enter Tag ID to delete: ")

            confirmation = input(
                f"Type DELETE to confirm removal of {tag_id}: "
            )

            if confirmation == "DELETE":
                deleted = delete_tag(tag_id)
                print(f"\n{deleted} deleted successfully.")
            else:
                print("Deletion cancelled.")

        else:
            print("Invalid option.")

    except ValueError as error:
        print("\nOperation failed:", error)


if __name__ == "__main__":
    main()
