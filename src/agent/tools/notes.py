import sqlite3
from pathlib import Path
DB_PATH = Path("data/notes.db")
def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
            """
        )
def add_note(content: str) -> dict:
    """
    Save a note in the SQLite database.
    """
    initialize_database()
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (content,),
        )
        note_id = cursor.lastrowid
    return {
        "id": note_id,
        "content": content,
    }
def list_notes() -> list[dict]:
    """
    Return all saved notes.
    """
    initialize_database()
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            "SELECT id, content FROM notes ORDER BY id"
        ).fetchall()
    return [
        {
            "id": row[0],
            "content": row[1],
        }
        for row in rows
    ]