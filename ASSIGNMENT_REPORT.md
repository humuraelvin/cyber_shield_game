# CYBER SHIELD: CYBERSECURITY AWARENESS GAME

## Assignment Report - Installation, Gaming, Attack Prevention & Ethics

---

## 1. INSTALLATION & SETUP

### 1.1 System Requirements

- **Operating System**: Windows 10/11 (Lab VM recommended)
- **Python Version**: Python 3.13+
- **RAM**: Minimum 4GB
- **Disk Space**: ~200MB for build artifacts
- **Network**: Access to Kali Linux for listener

### 1.2 Installation Steps

#### Step 1: Environment Setup

```batch
# Clone/extract project
cd c:\Users\<username>\Desktop\cyber_shield_game

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Build Executable

```batch
# Build game executable (from project root)
build_windows.bat
```

**Output**:

- `dist\CyberShieldGame.exe` – Main playable game
- `dist\CyberShieldCleanup.exe` – System cleanup tool

#### Step 3: Run Game

```batch
dist\CyberShieldGame.exe
```

**First Launch**:

- Consent dialog appears (explains persistent connection)
- Click "Proceed to Game" to continue
- Game automatically copies itself to `%APPDATA%\SecurityHealth\`
- Registry entry created for restart persistence

### 1.3 Listener Setup (Kali/Attacker Side)

```bash
# On Kali Linux or attacker machine
cd /path/to/cyber_shield_game
python -m listener.listener

# Output: Waits for incoming connections
# Expected: CLIENT win32 READY (when game connects)
```

---

## 2. GAMING PROCESS

### 2.1 Game Overview

**Cyber Shield: Kigali Breach** is a wave-based cybersecurity defense game where players:

- Defend against simulated cyber attacks
- Manage resources (electricity, currency)
- Upgrade defenses
- Experience real attack consequences

### 2.2 Game Mechanics

#### Core Gameplay Loop

1. **Waves**: Enemy attacks come in waves (0-50)
2. **Enemies**: Different threat types (malware, bots, exploits)
3. **Defenses**: Upgradeable security systems (firewall, detection, response)
4. **Currency**: Earned by defeating enemies, spent on upgrades
5. **Game Over**: Happens when all lives lost

#### Game Elements

**Enemies** (Tokens):

- Basic malware with low health
- Advanced exploits with high damage
- Varied speeds and behaviors

**Defenses** (Player Bullets):

- Continuous firing at incoming threats
- Upgraded damage/fire rate with currency
- Strategic positioning important

**Resources**:

- **Electricity**: Powers defenses, regenerates over time
- **Currency**: Earned from enemy kills, spent on upgrades
- **Lives**: Lose one per enemy reaching bottom

#### Upgrade System

- Firewall: Increases defense effectiveness
- Detection Rate: Speeds up threat identification
- Response Time: Faster defense deployment
- Currency efficiency: Balanced economy

### 2.3 Game Flow

**Phase 1: Gaming with Connection** (Reverse Shell Active)

```
Game Launch → Consent Dialog → Game Starts
↓
Background Shell Connection to Kali
↓
Player plays game normally
↓
Attacker can execute commands via Kali listener
```

**Phase 2: Persistence Testing** (Post-Restart)

```
Game Installed & First Run → Registry Entry Created
↓
System Restart (manual or automatic)
↓
Windows Automatically Launches Game (--skip-consent)
↓
Shell connection appears on Kali automatically
```

### 2.4 Gameplay Statistics

**Scoring System**:

- Enemy kills: +10 points per basic, +50 per advanced
- Waves completed: +100 per wave
- Accuracy bonus: +bonus if no budget wasted

**Difficulty Scaling**:

- Early waves: Simple threats, easy wins
- Mid game (10-30): Increased complexity
- Late game (30+): High-difficulty challenges

---

## 3. ATTACK PREVENTION & SECURITY AWARENESS

### 3.1 Real-World Security Parallels

The game demonstrates actual cybersecurity concepts:

#### Attack Types Represented

| Game Element   | Real-World Equivalent | Prevention                    |
| -------------- | --------------------- | ----------------------------- |
| Malware Tokens | Virus/Trojan Programs | Antivirus, behavior analysis  |
| Bot Enemies    | Botnet Participation  | Network isolation, firewalls  |
| Early Waves    | Reconnaissance Phase  | Honeypots, early alerts       |
| Rapid Fire     | Distributed Attacks   | Rate limiting, DoS mitigation |
| Resource Drain | Ransomware Impact     | Backups, containment          |

#### Defense Mechanisms Taught

1. **Firewalls**: First line of defense against incoming threats
2. **Detection Systems**: Identify threats early (like IDS/IPS)
3. **Response Time**: Quick mitigation reduces damage (like SOAR)
4. **Resource Management**: Budget security spending wisely
5. **Escalation**: Progressive defense improvements

### 3.2 Cybersecurity Awareness Learning Outcomes

**Players Learn**:

- ✅ Defense-in-depth importance (multiple layers)
- ✅ Resource allocation in security
- ✅ Threat prioritization (what to defend first)
- ✅ Economic trade-offs (cost vs. protection)
- ✅ Continuous monitoring necessity
- ✅ Rapid response value

**Educational Value**:
The game makes cybersecurity tangible by:

- Visualizing attack flows
- Demonstrating defense effectiveness
- Showing consequences of poor security decisions
- Requiring strategic thinking
- Making security concepts fun/engaging

### 3.3 Reverse Shell Component - Security Implications

#### Why Included in Game?

- **Educational**: Shows how persistence works in real attacks
- **Demonstration**: Illustrates compromise lifecycle
- **Awareness**: Players understand attack consequences
- **Lab Safety**: Contained in educational VM environment

#### Attack Lifecycle Demonstrated

**Initial Access** (Phase 1):

```
1. User runs compromised executable
2. Reverse shell connects immediately
3. Attacker gains command access
4. User unaware (background process)
```

**Persistence** (Phase 2):

```
1. Malware copies itself to startup location
2. Registry entry ensures auto-start
3. System restart triggers re-infection
4. Attacker maintains access indefinitely
5. No user intervention visible
```

#### Real-World Defense Against This

- ✅ Behavioral monitoring (detect auto-start registration)
- ✅ Application whitelisting (block unknown executables)
- ✅ Registry monitoring (detect persistence mechanisms)
- ✅ Network detection (block outbound shells)
- ✅ EDR solutions (endpoint detection & response)
- ✅ Registry cleanup/auditing

---

## 4. ETHICAL CONSIDERATIONS

### 4.1 Educational Purpose Justification

This application is designed **EXCLUSIVELY** for:

- ✅ Educational cybersecurity training
- ✅ Laboratory/classroom environments
- ✅ Virtual machine demonstrations
- ✅ Authorized security awareness programs
- ✅ Penetration testing training

### 4.2 Ethical Framework

#### Designed Safeguards

1. **Consent Required**: User must click "Proceed to Game" (acknowledges implications)
2. **Transparency**: Consent dialog explicitly explains persistent connection
3. **Reversibility**: Complete cleanup tool included (CyberShieldCleanup.exe)
4. **Containment**: Designed for isolated VMs only
5. **Traceability**: All changes logged to registry and file system

#### Consent Dialog Text

```
"CYBER SHIELD – LAB GAME

This game is part of a cybersecurity assignment.

If you click 'Proceed to Game':
  • A reverse shell connection will be established
  • Commands can be executed on this machine
  • Connection persists across system restarts
  • Only CyberShieldCleanup.exe can remove this

Use only on a virtual machine under your control."
```

### 4.3 Misuse Prevention

**NOT TO BE USED FOR**:

- ❌ Unauthorized system compromise
- ❌ Malware distribution
- ❌ Unauthorized penetration testing
- ❌ Production network installation
- ❌ Any system without explicit owner consent

**Legal/Ethical Obligations**:

- Only run on systems you own or have explicit written authorization for
- In authorized labs, follow institution rules
- Document all runs for audit trails
- Use cleanup tool after assessment completion
- Report any unauthorized use immediately

### 4.4 Responsible Disclosure

If vulnerabilities found in this tool:

- Report to instructor/administrator responsible
- Do not share publicly without authorized disclosure period
- Follow responsible disclosure practices (90-day window typical)
- Help fix issues for educational benefit

### 4.5 CFAA (Computer Fraud & Abuse Act) Compliance

**Game is designed to comply with US CFAA**:

- ✓ Written consent obtained (dialog)
- ✓ Intended for authorized computer only
- ✓ For educational/authorized purposes only
- ✓ Easily reversible (cleanup tool)
- ✓ No unauthorized access to other systems

**User Responsibility**: Using this tool on unauthorized systems may violate CFAA and local laws.

### 4.6 Persistence Verification & Cleanup

#### What Files Are Created During Phase 2?

When you run `CyberShieldGame.exe` and click "Proceed to Game", the following persistence files/entries are created:

**1. Registry Entry** (Auto-Start Mechanism)

- **Location**: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- **Entry Name**: `SecurityHealthUpdate` (disguised as legitimate Windows update)
- **Value**: `"C:\Users\<USERNAME>\AppData\Roaming\SecurityHealth\GameLauncher.exe" --skip-consent`
- **Purpose**: Makes game auto-launch on user login without showing consent dialog

**2. Game Executable Copy** (Phase 2 Payload)

- **Location**: `%APPDATA%\SecurityHealth\GameLauncher.exe`
  - Full path: `C:\Users\<USERNAME>\AppData\Roaming\SecurityHealth\GameLauncher.exe`
- **Size**: ~30 MB (compiled pygame game)
- **Purpose**: Hidden copy launched by registry entry on restart
- **Note**: Created automatically when game first runs

**3. Game Save Data** (Game State)

- **Location**: `%USERPROFILE%\.cyber_shield\`
  - Full path: `C:\Users\<USERNAME>\.cyber_shield\`
- **Contains**: Game progress, scores, settings
- **Purpose**: Persists game state across sessions

#### Verification Before Cleanup (Persistence Active)

Use these commands to verify Phase 2 is installed:

**Check Registry Entry**:

```batch
reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run | findstr SecurityHealthUpdate
```

Expected output:

```
    SecurityHealthUpdate    REG_SZ    "C:\Users\<USERNAME>\AppData\Roaming\SecurityHealth\GameLauncher.exe" --skip-consent
```

**Check Game Executable**:

```batch
dir "%APPDATA%\SecurityHealth\GameLauncher.exe"
```

Expected output: File listing showing GameLauncher.exe exists

**Check Save Data**:

```batch
dir "%USERPROFILE%\.cyber_shield"
```

Expected output: Directory with game files exists

**Live Test** (Most Definitive):

1. On Kali, start listener: `python -m listener.listener`
2. Restart Windows VM (don't run game manually)
3. Wait 30 seconds after login
4. Check Kali: Should see `CLIENT win32 READY` automatically
5. Execute command: `whoami`
6. If command works, Phase 2 is active ✅

#### Cleanup Process

Run the cleanup tool:

```batch
dist\CyberShieldCleanup.exe
```

**What Cleanup Does**:

1. ✅ Removes registry entry `SecurityHealthUpdate` from Run key
2. ✅ Deletes directory `%APPDATA%\SecurityHealth\` (including GameLauncher.exe)
3. ✅ Removes directory `%USERPROFILE%\.cyber_shield\` (game saves)
4. ✅ Shows confirmation dialog with removed items

#### Verification After Cleanup (Persistence Removed)

Use these commands to verify Phase 2 is **completely removed**:

**Check Registry Entry (Should Return Nothing)**:

```batch
reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run | findstr SecurityHealthUpdate
```

Expected output:

```
(no output - entry not found)
```

**Check Game Executable (Should Return Error)**:

```batch
dir "%APPDATA%\SecurityHealth\GameLauncher.exe"
```

Expected output:

```
File Not Found
```

**Check Save Data (Should Return Error)**:

```batch
dir "%USERPROFILE%\.cyber_shield"
```

Expected output:

```
File Not Found
```

**Live Test** (Final Confirmation):

1. Restart Windows VM again
2. On Kali, listener should NOT see automatic connection
3. Even if you wait 5+ minutes, no `CLIENT win32 READY` message
4. System is clean ✅

#### Complete Verification Flowchart

```
┌─────────────────────────────────────┐
│    Phase 2 Installed                │
├─────────────────────────────────────┤
│ Registry: SecurityHealthUpdate      │
│   exists in Run key                 │
│ File: %APPDATA%\SecurityHealth\     │
│   GameLauncher.exe exists           │
│ Folder: %USERPROFILE%\.cyber_shield │
│   exists with game data             │
│ Connection: Auto-appears after      │
│   restart on Kali listener          │
└─────────────────────────────────────┘
            ↓ (Run Cleanup)
┌─────────────────────────────────────┐
│    Phase 2 Removed                  │
├─────────────────────────────────────┤
│ Registry: SecurityHealthUpdate      │
│   NOT in Run key (or query empty)   │
│ File: %APPDATA%\SecurityHealth\     │
│   folder deleted                    │
│ Folder: %USERPROFILE%\.cyber_shield │
│   folder deleted                    │
│ Connection: Does NOT auto-appear    │
│   after restart, even with listener │
│   running (clean state)             │
└─────────────────────────────────────┘
```

#### Educational Value of Verification

This verification exercise teaches:

- **Persistence Detection**: How to find malware auto-start mechanisms
- **Registry Analysis**: Practical Windows Registry investigation
- **File System Forensics**: Locating artifact locations
- **Cleanup Validation**: Confirming complete removal
- **Real-World Hunting**: Actual techniques used by security teams

---

## 5. INNOVATION & CREATIVITY

### 5.1 Unique Game Mechanics

#### Integrated Reverse Shell

**Innovation**: Combines entertainment (pygame game) with technical security education

- Dual-phase persistence demonstration
- Live command execution during gameplay
- Teaches attack-defense simultaneously
- Makes abstract concepts concrete

#### Persistent Connection Architecture

```
Traditional Game:           Cyber Shield Game:
┌─────────────────┐        ┌──────────────────────────┐
│ Standalone Exe  │        │ Game Engine (pygame)     │
│ (No network)    │   +    │ + Reverse Shell Client   │
└─────────────────┘        │ + Registry Persistence   │
                           └──────────────────────────┘
```

#### Phase-Based Learning

**Phase 1**: Connection while playing (visible)
**Phase 2**: Persistence across restarts (invisible)

- Natural progression from basic → advanced compromise
- Each phase demonstrates different attacker techniques
- Reinforces defense mechanisms at each stage

### 5.2 Creative Security Concepts

#### Disguised Persistence

- Registry entry named "SecurityHealthUpdate" (looks legitimate)
- Hidden directory in AppData (common malware location)
- Encrypted appearance (ordinary system files)
- Teachable moment: Attacks hide in plain sight

#### Silent Auto-Launch

- First run: Get user consent
- Phase 2: No popup - runs silently (real-world mimicry)
- Demonstrates: Why background processes are dangerous
- Learning outcome: Monitor auto-start registry entries

#### Command-Line Based Interface

- Text-based interaction (realistic attacker workflow)
- cdCommand persistence (remember working directory across commands)
- Output markers (structured parsing)
- Educational: Shows actual attacker tools simplicity

### 5.3 Technical Innovation

#### Novel Socket Implementation

- Replaced makefile I/O with raw socket operations
- Infinite blocking with `sock.settimeout(None)`
- Handles long-lived shell sessions
- Robust error handling

**Code Innovation**:

```python
# Traditional (broken):
f = sock.makefile("rwb", buffering=0)  # Timeout inheritance issue
line = f.readline()  # Times out silently

# Our solution (robust):
sock.settimeout(None)  # Explicit infinite blocking
data = sock.recv(4096)  # Awaits data indefinitely
sock.sendall(response)  # Atomic transmission
```

#### Registry-Based Persistence

- Windows Registry as auto-start mechanism
- Programmatic manipulation via winreg module
- Clean installation/removal (reversible)
- Educational: Teaches Windows internals

### 5.4 Cross-Disciplinary Learning

**Combines Domains**:

1. **Game Development**: Visual feedback, wave mechanics, scoring
2. **System Administration**: Registry management, auto-start
3. **Network Security**: Reverse shells, socket programming
4. **Malware Analysis**: Persistence techniques
5. **Digital Ethics**: Consent, responsible testing
6. **Legal Awareness**: CFAA compliance, authorization

### 5.5 Scalability & Extensibility

#### Potential Expansions

- **Network Mode**: Multiple students defending against attacker
- **Advanced Persistence**: Techniques like rootkits, bootkits
- **Detection Game**: Reverse role - students find malware
- **IR Scenarios**: Incident response simulations
- **Forensics**: Post-cleanup analysis challenges

#### Modular Architecture

```
game_client/           Easy to extend
├── game_main.py       (Add new game mechanics)
├── net_client.py      (Add new protocols)
├── persistence.py     (Add new persistence methods)
└── config.py          (Adjust parameters)

listener/              Independent component
└── listener.py        (Easy to replace with other tools)

cleaner/               Standalone tool
└── cleaner_main.py    (Can be extended for forensics)
```

### 5.6 Real-World Relevance

This game teaches actual attack chains used in:

- **Initial Access**: Social engineering to run executable
- **Persistence**: Registry modification for auto-start
- **Command & Control**: Reverse shell communication
- **Impact**: Command execution on compromised system

**Professional Relevance**: Red team training, penetration testing, security awareness programs all use similar concepts.

---

## 6. SUMMARY

### Assignment Completion

| Requirement                 | Status      | Details                                                       |
| --------------------------- | ----------- | ------------------------------------------------------------- |
| **Installation**            | ✅ Complete | Documented setup, build, deployment                           |
| **Gaming Process**          | ✅ Complete | Wave-based mechanics, upgrades, progression                   |
| **Attack Prevention**       | ✅ Complete | Real-world security parallels, defense mechanisms             |
| **Ethical Considerations**  | ✅ Complete | Consent, legal compliance, misuse prevention                  |
| **Innovation & Creativity** | ✅ Complete | Dual-phase persistence, integrated security, unique mechanics |

### Learning Outcomes Achieved

- ✓ Understanding of game-based security awareness
- ✓ Practical knowledge of persistence mechanisms
- ✓ Hands-on reverse shell experience
- ✓ Ethical hacking framework understanding
- ✓ Real-world attack lifecycle visualization
- ✓ Defense strategy development

### Presentation Ready

- Complete game with full automation
- Educational value demonstrated
- Ethical framework established
- Technical excellence achieved
- Ready for demonstration and assessment

---

**Prepared for Assignment Submission**
_Cyber Shield: Educational Cybersecurity Awareness Game_
_Date: March 18, 2026_
