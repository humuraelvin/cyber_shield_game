import platform
from typing import Tuple


def check_runtime_dependencies() -> Tuple[bool, str]:
    """
    Perform lightweight checks to ensure the game can run smoothly
    on the target system.

    For PyInstaller builds most Python dependencies are bundled,
    so we mainly:
      - Record the OS
      - Optionally warn if not running on Windows for the backdoor demo
    """

    system = platform.system()

    if system != "Windows":
        # The game will still run, but the persistence + demo flow
        # is designed around Windows.
        return (
            True,
            "Running on a non‑Windows platform. The game will run, "
            "but the persistence demo is Windows‑only.",
        )

    # Everything else is bundled with the executable.
    return True, "All required runtime components appear to be available."

