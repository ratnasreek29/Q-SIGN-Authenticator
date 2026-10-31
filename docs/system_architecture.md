# System Architecture

Q-SIGN is organized into acquisition, processing, authentication, persistence,
registration, evaluation, and dashboard packages under `software/`.

The current workflow simulates RGB readings, derives ratio-based fingerprints,
and compares them with CSV reference data. Product-to-tag registrations are
stored in `software/data/product_registry.csv`. `database_manager.py` can
initialize the optional SQLite schema in `software/data/qsign.db`.

The ESP32 interface and dashboard are placeholders; the current prototype does
not acquire readings from physical hardware or serve a web interface.
