import os
import sys
from pathlib import Path
from typing import List, Tuple


STARTUP_VBS_NAME = "CyberShield_AutoStart.vbs"


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
    Create a small .vbs file in the Startup folder that will run the
    current executable silently (no window) with the --silent flag.
    """
    startup_dir = _get_startup_dir()
    try:
        startup_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return False, f"Failed to create startup directory: {exc!r}"

    target = Path(sys.executable)
    vbs_path = startup_dir / STARTUP_VBS_NAME

    # This VBS script runs the executable with --silent and 0 (hidden window)
    vbs_content = (
        'Set WshShell = CreateObject("WScript.Shell")\n'
        f'WshShell.Run chr(34) & "{target}" & chr(34) & " --silent", 0\n'
        'Set WshShell = Nothing\n'
    )

    try:
        with vbs_path.open("w", encoding="utf-8") as f:
            f.write(vbs_content)
    except OSError as exc:
        return False, f"Failed to write startup entry: {exc!r}"

    return True, f"Startup entry created at: {vbs_path}"


def remove_startup_entry() -> Tuple[bool, List[str]]:
    """
    Remove the .vbs file that was created for persistence.
    """
    startup_dir = _get_startup_dir()
    removed: List[str] = []
    vbs_path = startup_dir / STARTUP_VBS_NAME

    if vbs_path.exists():
        try:
            vbs_path.unlink()
            removed.append(str(vbs_path))
        except OSError:
            pass

    return bool(removed), removed

