
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "water_usage.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        conn.execute("""
            CREATE TABLE IF NOT EXISTS water_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usage_date TEXT,
                classroom TEXT,
                water_litres REAL,
                purpose TEXT,
                remarks TEXT
            )
        """)

        columns = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(water_usage)"
            ).fetchall()
        }

        # Add new columns without deleting old data
        new_columns = {
            "resource_type": "TEXT DEFAULT 'Water'",
            "resource_name": "TEXT DEFAULT 'Water'",
            "quantity": "REAL DEFAULT 0",
            "unit": "TEXT DEFAULT 'Litres'",
            "wastage_quantity": "REAL DEFAULT 0"
        }

        for column, data_type in new_columns.items():
            if column not in columns:
                conn.execute(
                    f"ALTER TABLE water_usage "
                    f"ADD COLUMN {column} {data_type}"
                )

        # Migrate older water records into the new format
        conn.execute("""
            UPDATE water_usage
            SET resource_type = 'Water',
                resource_name = 'Water',
                quantity = COALESCE(water_litres, 0),
                unit = 'Litres',
                wastage_quantity = COALESCE(wastage_quantity, 0)
            WHERE resource_type IS NULL
               OR resource_type = ''
        """)


def add_record(
    usage_date,
    classroom,
    resource_type,
    resource_name,
    quantity,
    unit,
    wastage_quantity,
    purpose,
    remarks
):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO water_usage (
                usage_date,
                classroom,
                water_litres,
                purpose,
                remarks,
                resource_type,
                resource_name,
                quantity,
                unit,
                wastage_quantity
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            usage_date,
            classroom,
            quantity if resource_type == "Water" else 0,
            purpose,
            remarks,
            resource_type,
            resource_name,
            quantity,
            unit,
            wastage_quantity
        ))


def get_records():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT *
            FROM water_usage
            ORDER BY usage_date DESC, id DESC
        """).fetchall()

        return [dict(row) for row in rows]
