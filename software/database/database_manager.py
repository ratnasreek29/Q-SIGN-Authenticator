import sqlite3
from contextlib import closing

from software.config import DATABASE_FILE


def initialize_database(path=DATABASE_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                optical_tag TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS fingerprints (
                sample_id TEXT PRIMARY KEY,
                r_g REAL NOT NULL,
                b_g REAL NOT NULL,
                r_b REAL NOT NULL
            );
            """
        )
    return path


if __name__ == "__main__":
    print(f"Initialized Q-SIGN database at {initialize_database()}")