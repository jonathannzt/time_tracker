# src/database.py

import sqlite3
from datetime import datetime

DB_NAME = "time_tracker.db"

class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._create_tables()

    def _create_tables(self):
        """Crée les tables si elles n'existent pas."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_name TEXT NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL NOT NULL
                )
            """)
            conn.commit()

    def insert_activity(self, process_name, start_time, end_time):
        """Insère un enregistrement d'activité."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO activities (process_name, start_time, end_time) VALUES (?, ?, ?)",
                (process_name, start_time, end_time)
            )
            conn.commit()

    def get_total_time_by_process(self):
        """
        Récupère la somme du temps par application (en secondes).
        Retourne un dict {process_name: total_seconds}.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query = """
                SELECT process_name, SUM(end_time - start_time)
                FROM activities
                GROUP BY process_name
            """
            cursor.execute(query)
            rows = cursor.fetchall()

        results = {}
        for row in rows:
            process_name, total_seconds = row
            results[process_name] = total_seconds
        return results

    def get_daily_report(self, date_str):
        """
        Par exemple, récupérer le temps total sur une journée donnée.
        Format de date_str = 'YYYY-MM-DD'.
        On peut se baser sur un timestamp min/max pour la journée.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # On calcule le timestamp min (00:00) et max (23:59) du jour
            day_start = datetime.strptime(date_str, "%Y-%m-%d").timestamp()
            day_end = day_start + 24*60*60 - 1  # 23:59:59

            query = """
                SELECT process_name, SUM(end_time - start_time)
                FROM activities
                WHERE start_time >= ? AND end_time <= ?
                GROUP BY process_name
            """
            cursor.execute(query, (day_start, day_end))
            rows = cursor.fetchall()

        results = {}
        for row in rows:
            process_name, total_seconds = row
            results[process_name] = total_seconds
        return results
