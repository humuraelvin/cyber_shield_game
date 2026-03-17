from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox

from game_client import persistence


SAVE_DIR = Path.home() / ".cyber_shield"


def run_cleanup():
    removed: list[str] = []

    if SAVE_DIR.exists():
        shutil.rmtree(SAVE_DIR, ignore_errors=True)
        removed.append(str(SAVE_DIR))

    ok, startup_removed = persistence.remove_startup_entry()
    if ok:
        removed.extend(startup_removed)

    return removed


def main():
    root = tk.Tk()
    root.withdraw()
    removed = run_cleanup()
    if removed:
        messagebox.showinfo(
            "Cyber Shield Cleanup",
            "Cleanup complete.\n\nRemoved:\n" + "\n".join(removed),
            parent=root,
        )
    else:
        messagebox.showinfo(
            "Cyber Shield Cleanup",
            "Nothing to remove.\nNo local Cyber Shield data or persistence entries were found.",
            parent=root,
        )


if __name__ == "__main__":
    main()

