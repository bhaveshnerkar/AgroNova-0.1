import sqlite3
import json
from datetime import datetime

DB_PATH = "agronova.db"

def init_db():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            location TEXT,
            temperature REAL,
            rainfall REAL,
            soil_type TEXT,
            water_level TEXT,
            recommended_crops TEXT,
            selected_crop TEXT,
            language TEXT DEFAULT 'english'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            timestamp TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            language TEXT DEFAULT 'english',
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def save_session(data: dict) -> int:
    """Save a farmer session and return session ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions 
        (created_at, location, temperature, rainfall, soil_type, water_level, recommended_crops, language)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        data.get("location", ""),
        data.get("temperature", 0),
        data.get("rainfall", 0),
        data.get("soil_type", ""),
        data.get("water_level", ""),
        json.dumps(data.get("recommended_crops", [])),
        data.get("language", "english")
    ))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def update_selected_crop(session_id: int, crop_key: str):
    """Update session with selected crop"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE sessions SET selected_crop = ? WHERE id = ?",
        (crop_key, session_id)
    )
    conn.commit()
    conn.close()

def save_chat(session_id: int, role: str, message: str, language: str = "english"):
    """Save a chat message"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_logs (session_id, timestamp, role, message, language)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, datetime.now().isoformat(), role, message, language))
    conn.commit()
    conn.close()

def get_session(session_id: int) -> dict:
    """Get session data by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "created_at": row[1],
        "location": row[2],
        "temperature": row[3],
        "rainfall": row[4],
        "soil_type": row[5],
        "water_level": row[6],
        "recommended_crops": json.loads(row[7]) if row[7] else [],
        "selected_crop": row[8],
        "language": row[9]
    }
