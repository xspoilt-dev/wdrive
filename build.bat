@echo off
REM Build script for wdrive - Creates standalone executable for Windows

echo 🚀 Building wdrive executable...

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 📦 Installing PyInstaller...
    pip install pyinstaller
)

REM Create build directory
if not exist build mkdir build
if not exist dist mkdir dist

echo 🔨 Building executable...

REM Build the executable
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "wdrive" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "requirements.txt;." ^
    --add-data "config.ini;." ^
    --add-data "README.md;." ^
    --add-data "LICENSE;." ^
    --hidden-import "dns" ^
    --hidden-import "dns.resolver" ^
    --hidden-import "dnslib" ^
    --hidden-import "qrcode" ^
    --hidden-import "PIL" ^
    --hidden-import "watchdog" ^
    run.py

if %errorlevel% equ 0 (
    echo ✅ Build successful!
    echo 📁 Executable created: dist\wdrive.exe
    echo.
    echo To run: dist\wdrive.exe
    echo.
    echo 📋 Build info:
    dir dist\wdrive.exe
) else (
    echo ❌ Build failed!
    exit /b 1
)

pause
