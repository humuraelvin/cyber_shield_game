### Cyber Shield: Kigali Breach – Backdoor Game Assignment

This project implements a **beautiful, fast-paced GUI game** built with `pygame` plus a **controlled reverse-shell demo** for your cybersecurity assignment.

- The Windows player runs **one game executable**: `CyberShieldGame.exe`.
- You (on Kali) run the **listener** and receive an interactive shell when the game starts.
- Persistence (auto-start on login) is available and **fully removable** via a second executable: `CyberShieldCleanup.exe`.
- Everything is transparent and documented, designed for **educational use in VMs only**.

---

### 1. Architecture overview

- `src/main.py` – core game: **Cyber Shield: Kigali Breach** (highly polished UI/UX).
- `game_client/game_main.py` – Windows entry point:
  - Tkinter consent + warnings.
  - Lightweight dependency/environment check.
  - Optional persistence install (Startup folder `.bat`).
  - Starts background reverse-shell client.
  - Launches the main `pygame` game.
- `game_client/net_client.py` – background TCP client that connects back to Kali and executes shell commands.
- `game_client/persistence.py` – Windows Startup-folder based persistence helpers (install/remove).
- `game_client/deps_check.py` – runtime environment checks.
- `game_client/config.py` – where you set `LISTENER_HOST` (your Kali IP) and port.
- `listener/listener.py` – Kali-side TCP listener that gives you a `shell>` prompt.
- `cleaner/cleaner_main.py` – Windows GUI cleaner:
  - Shows everything removed (save data, startup entries).
  - Allows the user to fully clean the system.
- `build_windows.bat` – builds **exactly two** Windows `.exe` files.
- `build_instructions.md` – detailed build steps.

---

### 2. Ethical and legal usage

This project is for the **Rwanda Coding Academy cybersecurity course**:

- Use **only** in:
  - Virtual machines.
  - Lab environments you fully control.
  - With informed consent of all participants.
- The game shows a **clear consent dialog** explaining that:
  - A remote shell connection will be opened to a listener.
  - Optional persistence can be installed.
  - A separate cleaner is provided.
- The code **does not try to evade antivirus** or hide; it is transparent by design.

---

### 3. Installation – Kali (listener + build environment)

From your Kali machine:

```bash
cd /home/humura/Documents/workings/Year\ 3/cybersec/cyber_shield
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

You now have everything to:

- Run the **listener**.
- Build Linux dev binaries.
- Prepare for building Windows `.exe` files.

---

### 4. Configuring the listener address

Edit `game_client/config.py`:

```python
LISTENER_HOST: str = "YOUR_KALI_IP"
LISTENER_PORT: int = 5050
```

Use the same port in `listener/listener.py` (default is `5050`).

---

### 5. Running the listener (Kali)

In your activated virtual environment:

```bash
python -m listener.listener
```

You will see:

- A message like: `[+] Listening on 0.0.0.0:5050 (Ctrl+C to stop)`.
- When the Windows game connects, connection info and a `shell>` prompt appear.
- Type commands at `shell>`; outputs are streamed back between `--- output start ---` and `--- output end ---`.

---

### 6. Building the two Windows executables

See `build_instructions.md` for full details. Summary (inside Windows VM):

1. Install Python and `pip install -r requirements.txt` and `pip install pyinstaller`.
2. From project root, run:

   ```bat
   build_windows.bat
   ```

3. After it finishes, you get in `dist\`:
   - `CyberShieldGame.exe`
   - `CyberShieldCleanup.exe`

Those are the **only two files** you give to the Windows user.

---

### 7. Game flow for the Windows user

1. Double-click `CyberShieldGame.exe`.
2. A **Tkinter consent dialog** appears:
   - Explains the reverse-shell behaviour.
   - Mentions that persistence can be enabled.
   - Mentions the cleaner executable.
3. After accepting:
   - Environment/dependency info is shown.
   - User can choose to enable persistence:
     - A `.bat` file is added to the Startup folder so the client/game runs automatically at logon (until cleaned).
4. The **full-screen Cyber Shield game** starts:
   - Neon grid background, smooth animations.
   - Rich HUD (agent name, waves, combo, HP, energy).
   - Enemies, tokens, dashes, special attacks – no interruptions while playing.
5. In the background:
   - The reverse-shell client (`ShellClient`) connects to your Kali listener.
   - You get a `shell>` prompt to run commands on the Windows machine.

> The player experiences a professional, immersive game. You demonstrate how a game can double as a backdoor when misused, while keeping everything transparent.

---

### 8. Persistence details

- Implemented via **Startup folder**:
  - A `.bat` file pointing to the built executable is placed in:
    - `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`
  - On non-Windows systems it falls back to a harmless directory in the user home.
- Installed only after:
  - The user accepts the initial consent.
  - The user clicks **YES** on the persistence prompt.
- Removed by:
  - `CyberShieldCleanup.exe` calling `persistence.remove_startup_entry()` and reporting what was deleted.

---

### 9. Cleaner executable behaviour

When the user runs `CyberShieldCleanup.exe`:

- A GUI window (Tkinter) opens silently in the background with dialog boxes:
  - It removes:
    - Local save data in `~/.cyber_shield`.
    - The Startup `.bat` file used for persistence (if present).
  - It shows a **beautiful summary dialog**:
    - Title: _Cyber Shield Cleanup_.
    - Body: list of all paths removed or a message that nothing was found.
- After cleanup, the system:
  - No longer auto-starts the client/game.
  - No longer keeps local Cyber Shield data.

---

### 10. Testing with Wine on Kali

After copying the two built `.exe` files back to Kali you can test:

```bash
source .venv/bin/activate
python -m listener.listener   # in one terminal
wine dist/CyberShieldGame.exe # in another terminal
```

You should see:

- Consent dialog (Wine window).
- Game launching and playable.
- Listener shows a new connection and accepts commands.

> For final presentation, repeat the same workflow using a Windows 10/11 VM as the target.

---

### 11. Report and marking alignment

Use this repository plus your slides/report to cover:

- **Game Functionality (25 pts)**:
  - Clear user notification and consent.
  - Dependency checks and environment info.
  - Smooth, uninterrupted gameplay.
  - Working reverse shell to the listener while game runs.
- **Persistence & Security (5 pts)**:
  - Startup-folder based persistence with clear prompts.
- **User Protection (5 pts)**:
  - Fully functioning GUI cleaner (`CyberShieldCleanup.exe`).
- **Documentation (5 pts)**:
  - This `README.md` and `build_instructions.md` explain installation, game flow, attack prevention, and ethics.
- **Innovation & Creativity (5 pts)**:
  - Unique cyber-defense arcade gameplay.
  - Strong visual style and UX.
  - Integrated security-awareness messaging via dialogs and help screens.

---

### 12. Persistence Files Verification

#### Files Created During Phase 2 Installation

When you run `CyberShieldGame.exe` and click "Proceed to Game", the following are created:

**Registry Entry** (Auto-Start Mechanism):

- Location: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Entry Name: `SecurityHealthUpdate`
- Verify: `reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run | findstr SecurityHealthUpdate`

**Game Executable Copy**:

- Location: `%APPDATA%\SecurityHealth\GameLauncher.exe`
- Verify: `dir "%APPDATA%\SecurityHealth\GameLauncher.exe"`

**Game Save Data**:

- Location: `%USERPROFILE%\.cyber_shield\`
- Verify: `dir "%USERPROFILE%\.cyber_shield"`

#### Verification Before Cleanup

Run these commands to confirm Phase 2 is active:

```batch
# Check registry entry exists
reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run | findstr SecurityHealthUpdate

# Check game executable exists
dir "%APPDATA%\SecurityHealth\GameLauncher.exe"

# Check save data exists
dir "%USERPROFILE%\.cyber_shield"

# Live test: On Kali listener, you should see automatic connection after system restart
```

#### Verification After Cleanup

Run these commands to confirm all persistence is removed:

```batch
# Registry entry should NOT exist (returns nothing)
reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run | findstr SecurityHealthUpdate

# Game executable should NOT exist (returns File Not Found)
dir "%APPDATA%\SecurityHealth\GameLauncher.exe"

# Save data should NOT exist (returns File Not Found)
dir "%USERPROFILE%\.cyber_shield"

# Live test: On Kali listener after restart, NO automatic connection appears
```

#### For Full Details

See **ASSIGNMENT_REPORT.md** section 4.6 "Persistence Verification & Cleanup" for comprehensive verification flowchart and educational value.

---
