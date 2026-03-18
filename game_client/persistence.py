import os
import sys
from pathlib import Path
from typing import List, Tuple
try:
    from .config import get_migrated_path
except (ImportError, ValueError):
    try:
        from game_client.config import get_migrated_path
    except ImportError:
        try:
            from config import get_migrated_path  # type: ignore
        except ImportError:
            def get_migrated_path(): from pathlib import Path; return Path.home()


STARTUP_BAT_NAME = "CyberShield_AutoStart.bat"
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

    # Remove any old .bat entry first to avoid duplicate startups
    old_bat = startup_dir / STARTUP_BAT_NAME
    if old_bat.exists():
        try:
            old_bat.unlink()
        except OSError:
            pass

    # Always point to the migrated path for the startup entry
    target = get_migrated_path()
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
    Remove both the .vbs and the legacy .bat files that were created for persistence.
    """
    startup_dir = _get_startup_dir()
    removed: List[str] = []
    
    for name in [STARTUP_VBS_NAME, STARTUP_BAT_NAME]:
        p = startup_dir / name
        if p.exists():
            try:
                p.unlink()
                removed.append(str(p))
            except OSError:
                pass

    return bool(removed), removed

