# src/config.py

import json
import os

DEFAULT_CONFIG = {
    "update_interval": 1,
    "refresh_interval": 1000 
}

CONFIG_FILE = "config.json"

def load_config():
    """Charge la config depuis config.json, sinon crée un fichier par défaut."""
    if not os.path.isfile(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_config(config):
    """Sauvegarde la config dans config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
