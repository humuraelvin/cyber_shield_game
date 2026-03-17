#!/usr/bin/env bash
set -e
python3 -m PyInstaller --noconfirm --clean --onedir --windowed --name CyberShieldGameLinux src/main.py
echo
echo "Linux developer build complete: dist/CyberShieldGameLinux/"
