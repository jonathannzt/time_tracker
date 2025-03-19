# src/tracker.py

import time
import threading
import win32gui
import win32process
import psutil
from datetime import datetime
from src.database import DatabaseManager

class TimeTracker:
    def __init__(self, update_interval=1):
        self.update_interval = update_interval
        self._running = False
        self._thread = None
        self._db = DatabaseManager()

        self._current_process = None
        self._start_time = None

    def _get_active_window_process(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except Exception:
            return None

    def _tracking_loop(self):
        while self._running:
            time.sleep(self.update_interval)
            process_actif = self._get_active_window_process()
            current_time = time.time()

            if process_actif != self._current_process:
                if self._current_process is not None and self._start_time is not None:
                    self._db.insert_activity(self._current_process, self._start_time, current_time)

                self._current_process = process_actif
                self._start_time = current_time

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._tracking_loop, daemon=True)
            self._thread.start()

    def stop(self):
        if self._running:
            self._running = False
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=2)

            if self._current_process is not None and self._start_time is not None:
                self._db.insert_activity(self._current_process, self._start_time, time.time())

            self._current_process = None
            self._start_time = None
            self._thread = None

    def get_activities(self):
        """
        Récupère la somme des temps (en secondes) par application,
        en interrogeant la DB.
        """
        return self._db.get_total_time_by_process()
