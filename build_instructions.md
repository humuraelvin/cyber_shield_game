### Build and packaging instructions

This project is designed so that you ship **exactly two Windows executables**:

- `CyberShieldGame.exe` – the beautiful game + consent + reverse shell + optional persistence
- `CyberShieldCleanup.exe` – the GUI cleanup tool that removes local data and persistence

All other files stay on your Kali / developer machine.

---

### 1. Python environment on Kali

1. Create and activate a virtual environment (recommended):

   ```bash
   cd /home/humura/Documents/workings/Year\ 3/cybersec/cyber_shield
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install pyinstaller
   ```

---

### 2. Configure the listener IP and port

Edit `game_client/config.py` and set `LISTENER_HOST` to the IP address of your Kali machine (the one that will run the listener):

```python
LISTENER_HOST: str = "192.168.56.10"  # example: your Kali IP
LISTENER_PORT: int = 5050
```

Use the same port when starting the listener.

---

### 3. Build the Windows executables

On a Windows 10/11 VM (recommended for clean builds):

1. Clone or copy the project into the Windows VM.
2. Install Python for Windows and `pip install -r requirements.txt` and `pip install pyinstaller`.
3. From a **Developer Command Prompt** or `cmd` in the project root, run:

   ```bat
   build_windows.bat
   ```

This produces in `dist\`:

- `CyberShieldGame.exe`
- `CyberShieldCleanup.exe`

> You can also try to run `build_windows.bat` under Wine on Kali, but for clean marking, building inside a Windows VM is more reliable.

---

### 4. Running the listener on Kali

On Kali (or any Linux you control), inside your virtual environment:

```bash
source .venv/bin/activate
python -m listener.listener
```

By default this listens on `0.0.0.0:5050`. You can then type commands at the `shell>` prompt once the Windows game connects.

---

### 5. Testing with Wine on Kali

After building on Windows and copying the two `.exe` files back to Kali:

```bash
wine dist/CyberShieldGame.exe
```

This lets you test:

- Consent dialog
- Environment checks
- Game launching and play
- Reverse shell connection back to `listener.py`

For final marking, use a Windows VM as the target machine.

