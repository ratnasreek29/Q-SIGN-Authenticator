
import sqlite3
from datetime import datetime, timezone

from software.config import DATABASE_FILE


def get_connection():
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_FILE)


def initialize_history():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS verification_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                product_id TEXT,
                tag_id TEXT NOT NULL,
                red INTEGER NOT NULL,
                green INTEGER NOT NULL,
                blue INTEGER NOT NULL,
                distance REAL NOT NULL,
                threshold REAL NOT NULL,
                result TEXT NOT NULL
            )
        """)


def save_history(
    source,
    tag_id,
    rgb,
    distance,
    threshold,
    possible_match,
    product_id=None,
):
    initialize_history()

    result = (
        "POSSIBLE MATCH"
        if possible_match
        else "FINGERPRINT MISMATCH"
    )

    timestamp = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO verification_history (
                timestamp, source, product_id, tag_id,
                red, green, blue, distance, threshold, result
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                source,
                product_id,
                tag_id,
                int(rgb[0]),
                int(rgb[1]),
                int(rgb[2]),
                float(distance),
                float(threshold),
                result,
            ),
        )


def load_history():
    initialize_history()

    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT *
            FROM verification_history
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]
