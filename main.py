# main.py

from src.tracker import TimeTracker
from src.gui import App
from src.config import load_config

def main():
    cfg = load_config()
    tracker = TimeTracker(update_interval=cfg["update_interval"])
    app = App(tracker, refresh_interval=cfg["refresh_interval"])
    app.mainloop()

if __name__ == "__main__":
    main()