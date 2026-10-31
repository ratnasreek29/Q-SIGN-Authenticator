from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SOFTWARE_DIR.parent
DATA_DIR = SOFTWARE_DIR / "data"
READINGS_FILE = DATA_DIR / "readings.csv"
FINGERPRINTS_FILE = DATA_DIR / "fingerprints.csv"
PRODUCT_REGISTRY_FILE = DATA_DIR / "product_registry.csv"
DATABASE_FILE = DATA_DIR / "qsign.db"
MATCH_THRESHOLD = 0.10