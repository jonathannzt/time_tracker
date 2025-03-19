# src/gui.py

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from src.tracker import TimeTracker

class App(tk.Tk):
    def __init__(self, tracker, refresh_interval=1000):
        super().__init__()
        self.tracker = tracker
        self.refresh_interval = refresh_interval
        self.title("Time Tracker")
        self.geometry("500x400")
        
        self.tree = ttk.Treeview(self, columns=("process", "time"), show="headings")
        self.tree.heading("process", text="Application")
        self.tree.heading("time", text="Temps (HH:MM:SS)")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=5)

        self.start_button = tk.Button(self.btn_frame, text="Démarrer", command=self.start_tracking)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.btn_frame, text="Arrêter", command=self.stop_tracking)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.graph_button = tk.Button(self, text="Afficher Graphique", command=self.show_graph)
        self.graph_button.pack(pady=5)

        self.after(self.refresh_interval, self.update_ui)

    def show_graph(self):
        """Affiche un graphique (camembert) du temps passé par application."""
        activities = self.tracker.get_activities()
        labels = list(activities.keys())
        values = list(activities.values())

        if not labels or not values:
            return

        plt.figure("Répartition du temps par application")
        plt.pie(values, labels=labels, autopct='%1.1f%%') 
        plt.title("Répartition du temps d'utilisation")
        plt.show()

    def start_tracking(self):
        """Démarre le tracking."""
        self.tracker.start()

    def stop_tracking(self):
        """Arrête le tracking."""
        self.tracker.stop()

    def update_ui(self):
        """
        Met à jour l'affichage de la liste des applications et du temps utilisé,
        puis programme le prochain rafraîchissement.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        activities = self.tracker.get_activities()

        for process_name, total_seconds in activities.items():
            temps_formate = self._format_time(total_seconds)
            self.tree.insert("", "end", values=(process_name, temps_formate))

        self.after(self.refresh_interval, self.update_ui)

    def _format_time(self, seconds):
        """Convertit un nombre de secondes en HH:MM:SS (string)."""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02}"
