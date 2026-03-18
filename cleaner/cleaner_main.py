import sys
import os
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox

# Import persistence cleanup
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from game_client.persistence import remove_persistence
except ImportError:
    try:
        from persistence import remove_persistence
    except ImportError:
        def remove_persistence():
            return False, "Persistence module not available"

SAVE_DIR = Path.home() / ".cyber_shield"


def run_cleanup():
    removed: list[str] = []

    # 1) Remove registry persistence (Phase 2)
    if sys.platform == "win32":
        try:
            ok, msg = remove_persistence()
            if ok:
                removed.append(msg)
        except Exception as e:
            removed.append(f"Registry cleanup: {e}")

    # 2) Remove hidden shell executable
    if sys.platform == "win32":
        shell_dir = Path.home() / "AppData" / "Roaming" / "SecurityHealth"
    else:
        shell_dir = Path.home() / ".local" / "share" / "SecurityHealth"
    
    if shell_dir.exists():
        try:
            shutil.rmtree(shell_dir, ignore_errors=True)
            removed.append(f"Removed: {shell_dir}")
        except Exception:
            pass

    # 3) Remove local save data
    if SAVE_DIR.exists():
        try:
            shutil.rmtree(SAVE_DIR, ignore_errors=True)
            removed.append(f"Removed: {SAVE_DIR}")
        except Exception:
            pass

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
