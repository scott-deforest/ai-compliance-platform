import sqlite3
from pathlib import Path
from datetime import datetime


DB_PATH = Path(__file__).resolve().parent.parent / "audit.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    print(f"Using audit database: {DB_PATH}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        workflow_type TEXT,
        user_input TEXT,
        ai_output TEXT,
        human_decision TEXT,
        reviewer_notes TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_audit_log():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, workflow_type, user_input, ai_output, human_decision, reviewer_notes FROM audit_log ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def log_interaction(
    workflow_type: str,
    user_input: str,
    ai_output: str,
    human_decision: str,
    reviewer_notes: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO audit_log (
        timestamp,
        workflow_type,
        user_input,
        ai_output,
        human_decision,
        reviewer_notes
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        workflow_type,
        user_input,
        ai_output,
        human_decision,
        reviewer_notes,
    ))

    conn.commit()
    conn.close()