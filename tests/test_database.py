import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from software.database.database_manager import initialize_database


class DatabaseTests(unittest.TestCase):
    def test_initializes_product_and_fingerprint_tables(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "qsign.db"
            initialize_database(database_path)

            with closing(sqlite3.connect(database_path)) as connection:
                tables = {
                    row[0]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }

        self.assertIn("products", tables)
        self.assertIn("fingerprints", tables)


if __name__ == "__main__":
    unittest.main()