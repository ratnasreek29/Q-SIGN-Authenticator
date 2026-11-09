import csv

from software.config import PRODUCT_REGISTRY_FILE


def load_product_registry(path=PRODUCT_REGISTRY_FILE):
    if not path.exists():
        return {}

    with path.open("r", newline="") as file:
        return {
            row["Product_ID"]: row["Optical_Tag"]
            for row in csv.DictReader(file)
        }


def register_product(product_id, optical_tag, path=PRODUCT_REGISTRY_FILE):
    product_id = product_id.strip().upper()
    optical_tag = optical_tag.strip().upper()
    if not product_id or not optical_tag:
        raise ValueError("Product ID and optical tag cannot be empty.")

    products = load_product_registry(path)
    if product_id in products:
        raise ValueError(f"Product ID {product_id} is already registered.")

    file_exists = path.exists() and path.stat().st_size > 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Product_ID", "Optical_Tag"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"Product_ID": product_id, "Optical_Tag": optical_tag})

    return product_id, optical_tag