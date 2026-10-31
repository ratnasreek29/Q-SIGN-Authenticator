# Q-SIGN Authenticator
### Quantum-Dot-Based Optical Fingerprinting System for Product Authentication

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

The current software prototype consists of the following stages:

### 1. Dataset Generation
`sensor_simulator.py`

Generates simulated RGB readings for different optical tags and stores them in `readings.csv`.

### 2. Dataset Analysis
- `dataset_analysis.py` – Displays the generated dataset.
- `average_analysis.py` – Calculates average sensor readings for each tag.

### 3. Fingerprint Extraction
`feature_extraction.py`

Extracts three numerical features from average RGB readings:

- R/G ratio
- B/G ratio
- R/B ratio

The extracted fingerprints are stored in `fingerprints.csv`.

### 4. Reference Database
`reference_database.py`

Loads and organises the stored optical fingerprints for further comparison.

### 5. Fingerprint Matching
- `fingerprint_matching.py` – Compares a scanned fingerprint with stored fingerprints.
- `threshold_matching.py` – Uses a distance threshold to classify a fingerprint.
- `test_unknown.py` – Allows manual testing with RGB values.

### 6. Performance Evaluation
- `performance_evaluation.py` – Evaluates fingerprint matching using calibration and test readings.
- `confusion_matrix.py` – Displays classification results using a confusion matrix.

### 7. Product Registration and Authentication
- `register_product.py` – Associates product IDs with available optical tags.
- `product_authentication.py` – Retrieves the expected fingerprint and compares it with the scanned RGB readings.

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
2. Open the `software` folder in VS Code.
3. Open the integrated terminal.
4. Run the following commands in sequence:

```bash
python sensor_simulator.py
python dataset_analysis.py
python average_analysis.py
python feature_extraction.py
python reference_database.py
```

5. Test fingerprint matching:

```bash
python fingerprint_matching.py
python threshold_matching.py
```

6. Evaluate the prototype:

```bash
python performance_evaluation.py
python confusion_matrix.py
```

7. Register a product:

```bash
python register_product.py
```

8. Authenticate a registered product:

```bash
python product_authentication.py
```

Note: Run these commands from inside the `software` directory. The simulator generates the readings used by the subsequent scripts. Register products before attempting product authentication.

## Current Development Status

The current implementation is a software proof of concept.

- Simulated RGB readings are used for testing.
- Fingerprint features are extracted from RGB ratios.
- Reference fingerprints are stored in CSV files.
- Product IDs are linked to optical tags.
- Product-specific fingerprint matching is implemented.

Actual quantum-dot measurements and physical sensor-based authentication have not yet been integrated.

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
