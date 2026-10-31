# Q-SIGN Authenticator
### Quantum-Dot-Based Optical Fingerprinting System for Product Authentication

###handwritten (dont use ai in this section)### -
to run it - python -m software.main
to run test - python -m unittest discover -s tests


## About the Project

Q-SIGN is a product-authentication prototype that explores the use of quantum-dot-based optical markers to create optical fingerprints for product verification.

The project aims to develop an alternative approach to product authentication by analysing the optical properties of a marker rather than relying solely on conventional identifiers such as QR codes, serial numbers and printed labels.

## Problem Statement

Counterfeit products can imitate conventional authentication methods, including printed labels, QR codes and serial numbers.

Q-SIGN explores whether optical fingerprints generated from quantum-dot-based markers can provide an additional method of checking product identity.

## Proposed Solution

The proposed system follows this process:

1. A UV light source illuminates the quantum-dot-based optical marker.
2. The marker emits visible fluorescence.
3. An optical sensor measures the emitted light.
4. RGB readings are processed using Python.
5. Numerical features are extracted to generate an optical fingerprint.
6. The scanned fingerprint is compared with the stored reference fingerprint associated with the product.
7. The software displays the authentication result.

## System Architecture

**Hardware Components (Planned Integration)**
- ESP32 microcontroller
- TCS34725 RGB colour sensor
- 365 nm UV LED
- Quantum-dot-based optical marker
- OLED display

**Software Components**
- Python
- CSV-based data storage
- Feature extraction
- Euclidean distance-based fingerprint matching
- Product registration and authentication

## Software Workflow

The software is grouped by responsibility under `software/`:

### 1. Dataset Generation
`software/acquisition/sensor_simulator.py`

Generates simulated RGB readings for different optical tags and stores them in `readings.csv`.

### 2. Dataset Analysis
- `software/evaluation/dataset_analysis.py` – Displays the generated dataset.
- `software/processing/average_analysis.py` – Calculates average sensor readings for each tag.

### 3. Fingerprint Extraction
`software/processing/feature_extraction.py`

Extracts three numerical features from average RGB readings:

- R/G ratio
- B/G ratio
- R/B ratio

The extracted fingerprints are stored in `fingerprints.csv`.

### 4. Reference Database
`software/database/reference_database.py`

Loads and organises the stored optical fingerprints for further comparison.

### 5. Fingerprint Matching
- `software/authentication/fingerprint_matching.py` – Compares a scanned fingerprint with stored fingerprints.
- `software/authentication/threshold_matching.py` – Uses a distance threshold to classify a fingerprint.

### 6. Performance Evaluation
- `software/evaluation/performance_evaluation.py` – Evaluates fingerprint matching using calibration and test readings.
- `software/evaluation/confusion_matrix.py` – Displays classification results using a confusion matrix.

### 7. Product Registration and Authentication
- `software/registration/register_product.py` – Associates product IDs with available optical tags.
- `software/authentication/product_authentication.py` – Retrieves the expected fingerprint and compares it with scanned RGB readings.

## Fingerprint Matching Algorithm

The current prototype uses Euclidean distance to compare two optical fingerprints.

The distance is calculated as:

d = √[(A1 − B1)² + (A2 − B2)² + (A3 − B3)²]

Where:
- A represents the scanned fingerprint.
- B represents the stored reference fingerprint.
- d represents the distance between the two fingerprints.

A provisional threshold of 0.10 is currently used in the demonstration.

- Distance ≤ threshold: POSSIBLE MATCH
- Distance > threshold: FINGERPRINT MISMATCH

The threshold requires further calibration using actual hardware measurements.

## How to Run the Software

### Requirements
- Python 3
- Visual Studio Code (recommended)

### Steps

1. Clone or download this repository.
2. Open the repository root in VS Code and open a terminal there.
3. Run the following commands in sequence:

```bash
python -m software.acquisition.sensor_simulator
python -m software.evaluation.dataset_analysis
python -m software.processing.average_analysis
python -m software.processing.feature_extraction
python -m software.database.reference_database
```

5. Test fingerprint matching:

```bash
python -m software.authentication.fingerprint_matching
python -m software.authentication.threshold_matching
```

6. Evaluate the prototype:

```bash
python -m software.evaluation.performance_evaluation
python -m software.evaluation.confusion_matrix
```

7. Register a product:

```bash
python -m software.registration.register_product
```

8. Authenticate a registered product:

```bash
python -m software.authentication.product_authentication
```

Run all commands from the repository root. `python -m software.main` opens a simple workflow menu. The simulator generates readings for later steps; register products before attempting authentication. Run the tests with `python -m unittest discover -s tests`.

## Current Development Status

The current implementation is a software proof of concept.

- Simulated RGB readings are used for testing.
- Fingerprint features are extracted from RGB ratios.
- Reference fingerprints are stored in CSV files.
- Product IDs are linked to optical tags.
- Product-specific fingerprint matching is implemented.

Actual quantum-dot measurements and physical sensor-based authentication have not yet been integrated.

The ESP32 interface and dashboard modules are placeholders for future integration. The current workflow uses CSV files in `software/data`; `software/database/database_manager.py` can initialize the optional SQLite database.

## Future Scope

- Integration of ESP32 with the TCS34725 sensor.
- Direct acquisition of RGB readings from physical optical markers.
- Registration of additional optical tags.
- Calibration using actual quantum-dot fluorescence measurements.
- Improved fingerprint discrimination and threshold calibration.
- Testing under different illumination and measurement conditions.
- Development of a user-friendly authentication interface.

## Project Objective

To explore a hardware-software-based product authentication approach using optical fingerprinting and computational comparison.

---

**Project:** Q-SIGN Authenticator  
**Domain:** Artificial Intelligence and Machine Learning / Embedded Systems / Product Authentication  
**Programming Language:** Python  
**Development Stage:** Software Prototype
