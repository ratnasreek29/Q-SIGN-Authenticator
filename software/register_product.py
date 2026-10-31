
import csv
import os

# Step 1: Load available optical tags

available_tags = []

with open("fingerprints.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:
        available_tags.append(row["Sample_ID"])


# Step 2: Ask for product information

product_id = input("Enter new Product ID: ").strip().upper()

print("\nAvailable optical tags:")

for tag in available_tags:
    print("-", tag)

selected_tag = input("\nEnter optical tag: ").strip().upper()


# Step 3: Validate inputs

if not product_id:

    print("Product ID cannot be empty.")

elif selected_tag not in available_tags:

    print("Invalid optical tag.")

else:

    # Step 4: Create database if it doesn't exist

    file_exists = os.path.exists("product_registry.csv")

    existing_products = []

    if file_exists:

        with open("product_registry.csv", "r") as file:

            reader = csv.DictReader(file)

            existing_products = list(reader)


    # Step 5: Check duplicate Product IDs

    duplicate = any(
        product["Product_ID"] == product_id
        for product in existing_products
    )

    if duplicate:

        print("This Product ID is already registered.")

    else:

        # Step 6: Save product information

        with open(
            "product_registry.csv",
            "a",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=["Product_ID", "Optical_Tag"]
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "Product_ID": product_id,
                "Optical_Tag": selected_tag
            })

        print("\nProduct registered successfully!")
        print("Product ID:", product_id)
        print("Optical Tag:", selected_tag)
