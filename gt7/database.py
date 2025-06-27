import sqlite3
import logging

l = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file="sessions.db"):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            l.info(f"Connected to database: {self.db_file}")
        except sqlite3.Error as e:
            l.error(f"Error connecting to database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            l.info("Database connection closed.")

    def create_tables(self):
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                driver TEXT,
                vehicle TEXT,
                venue TEXT,
                session TEXT,
                best_lap REAL
            )
            """)
            self.conn.commit()
            l.info("Database tables created successfully.")
        except sqlite3.Error as e:
            l.error(f"Error creating tables: {e}")

    def insert_session(self, session_data):
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT INTO sessions (driver, vehicle, venue, session, best_lap)
            VALUES (?, ?, ?, ?, ?)
            """, (
                session_data.get("driver", ""),
                session_data.get("vehicle", ""),
                session_data.get("venue", ""),
                session_data.get("session", ""),
                session_data.get("best_lap", 0.0)
            ))
            self.conn.commit()
            l.info(f"New session inserted: {session_data}")
        except sqlite3.Error as e:
            l.error(f"Error inserting session: {e}")

    def get_sessions(self, limit=10):
        if not self.conn:
            self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM sessions ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            sessions = [dict(zip(columns, row)) for row in rows]
            return sessions
        except sqlite3.Error as e:
            l.error(f"Error getting sessions: {e}")
            return []
