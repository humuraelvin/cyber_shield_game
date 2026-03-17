@echo off
REM Build Windows executables for the Cyber Shield assignment.
REM Result: two .exe files to give to the Windows user:
REM   - dist\CyberShieldGame.exe
REM   - dist\CyberShieldCleanup.exe

py -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name CyberShieldGame game_client\game_main.py

py -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name CyberShieldCleanup cleaner\cleaner_main.py

echo.
echo Build complete. Files are in the dist\ folder:
echo   - CyberShieldGame.exe
echo   - CyberShieldCleanup.exe
pause
