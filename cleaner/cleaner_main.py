import sys
import os
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox

# Add the project root to sys.path so we can import game_client
# when running this script directly from the 'cleaner' directory.
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from game_client import persistence
except ImportError:
    # If bundled or moved, persistence might be in the same dir
    import persistence  # type: ignore


SAVE_DIR = Path.home() / ".cyber_shield"


def run_cleanup():
    removed: list[str] = []

    if SAVE_DIR.exists():
        # Remove lock file if it exists
        lock_file = SAVE_DIR / "client.lock"
        if lock_file.exists():
            try:
                lock_file.unlink()
                removed.append(str(lock_file))
            except OSError:
                pass

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

