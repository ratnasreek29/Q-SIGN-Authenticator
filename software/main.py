import subprocess
import sys


WORKFLOWS = {
    "1": ("Generate simulated readings", "software.acquisition.sensor_simulator"),
    "2": ("Inspect dataset", "software.evaluation.dataset_analysis"),
    "3": ("Calculate average readings", "software.processing.average_analysis"),
    "4": ("Extract fingerprints", "software.processing.feature_extraction"),
    "5": ("Match a sample fingerprint", "software.authentication.fingerprint_matching"),
    "6": ("Evaluate matching performance", "software.evaluation.performance_evaluation"),
    "7": ("Register a product", "software.registration.register_product"),
    "8": ("Authenticate a product", "software.authentication.product_authentication"),
}


def main():
    print("Q-SIGN AUTHENTICATOR")
    for key, (label, _) in WORKFLOWS.items():
        print(f"{key}. {label}")

    choice = input("Select a workflow: ").strip()
    if choice not in WORKFLOWS:
        print("Invalid workflow selection.")
        return

    subprocess.run(
        [sys.executable, "-m", WORKFLOWS[choice][1]],
        check=False,
    )


if __name__ == "__main__":
    main()