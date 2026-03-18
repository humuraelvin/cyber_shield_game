import sys
import os
import subprocess
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox

# Add the project root to sys.path so we can import game_client
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from game_client import persistence
    from game_client.config import get_migrated_path
except ImportError:
    import persistence  # type: ignore
    try:
        from config import get_migrated_path  # type: ignore
    except ImportError:
        def get_migrated_path(): return Path.home() # Fallback

SAVE_DIR = Path.home() / ".cyber_shield"


def run_cleanup():
    removed: list[str] = []

    # 1) Kill any running background client
    migrated_exe = get_migrated_path()
    if migrated_exe.name:
        try:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/IM", migrated_exe.name, "/T"], capture_output=True)
            else:
                subprocess.run(["pkill", "-f", migrated_exe.name], capture_output=True)
        except Exception:
            pass

    # 2) Remove migrated binary directory
    # We are careful not to delete important Windows directories
    migrated_dir = migrated_exe.parent
    if migrated_dir.exists() and "Microsoft" not in migrated_dir.parts:
         shutil.rmtree(migrated_dir, ignore_errors=True)
         removed.append(str(migrated_dir))
    elif migrated_exe.exists():
         try:
             migrated_exe.unlink()
             removed.append(str(migrated_exe))
         except OSError:
             pass

    # 3) Remove local save data and lock files
    if SAVE_DIR.exists():
        lock_file = SAVE_DIR / "client.lock"
        if lock_file.exists():
            try:
                lock_file.unlink()
                removed.append(str(lock_file))
            except OSError:
                pass

        shutil.rmtree(SAVE_DIR, ignore_errors=True)
        removed.append(str(SAVE_DIR))

    # 4) Remove startup items
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
