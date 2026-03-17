
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox

SAVE_DIR = Path.home() / ".cyber_shield"

def run_cleanup():
    removed = []
    if SAVE_DIR.exists():
        shutil.rmtree(SAVE_DIR, ignore_errors=True)
        removed.append(str(SAVE_DIR))
    return removed

def main():
    root = tk.Tk()
    root.withdraw()
    removed = run_cleanup()
    if removed:
        messagebox.showinfo("Cyber Shield Cleanup", "Cleanup complete.\n\nRemoved:\n" + "\n".join(removed))
    else:
        messagebox.showinfo("Cyber Shield Cleanup", "Nothing to remove.\nNo local Cyber Shield data was found.")

if __name__ == "__main__":
    main()
