import os
import sys
from pathlib import Path
from typing import List, Tuple


STARTUP_BAT_NAME = "CyberShield_AutoStart.bat"


def _get_startup_dir() -> Path:
    """
    Return the current user's Startup folder on Windows.

    On non‑Windows platforms this points to a harmless path in the
    user's home directory so that the functions are effectively no‑ops.
    """
    appdata = os.getenv("APPDATA")
    if not appdata:
        return Path.home() / ".cyber_shield_startup_sim"
    return Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"


def install_startup_entry() -> Tuple[bool, str]:
    """
    Create a small .bat file in the Startup folder that will run the
    current executable on user logon.

    This is intentionally simple and transparent for educational use.
    """
    startup_dir = _get_startup_dir()
    try:
        startup_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # noqa: BLE001
        return False, f"Failed to create startup directory: {exc!r}"

    target = Path(sys.executable)
    bat_path = startup_dir / STARTUP_BAT_NAME

    try:
        with bat_path.open("w", encoding="utf-8") as f:
            f.write(f"@echo off\n\"{target}\" %*\n")
    except OSError as exc:  # noqa: BLE001
        return False, f"Failed to write startup entry: {exc!r}"

    return True, f"Startup entry created at: {bat_path}"


def remove_startup_entry() -> Tuple[bool, List[str]]:
    """
    Remove the .bat file that was created for persistence.
    """
    startup_dir = _get_startup_dir()
    removed: List[str] = []
    bat_path = startup_dir / STARTUP_BAT_NAME

    if bat_path.exists():
        try:
            bat_path.unlink()
            removed.append(str(bat_path))
        except OSError:
            pass

    return bool(removed), removed

