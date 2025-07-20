#!/bin/bash
# Build script for wdrive - Creates standalone executables

echo "🚀 Building wdrive executable..."

# Check if PyInstaller is installed
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Create build directory
mkdir -p build dist

echo "🔨 Building executable..."

# Build the executable
pyinstaller \
    --onefile \
    --windowed \
    --name "wdrive" \
    --icon "static/favicon.ico" \
    --add-data "templates;templates" \
    --add-data "static;static" \
    --add-data "requirements.txt;." \
    --add-data "config.ini;." \
    --add-data "README.md;." \
    --add-data "LICENSE;." \
    --hidden-import "dns" \
    --hidden-import "dns.resolver" \
    --hidden-import "dnslib" \
    --hidden-import "qrcode" \
    --hidden-import "PIL" \
    --hidden-import "watchdog" \
    run.py

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📁 Executable created: dist/wdrive"
    echo ""
    echo "To run:"
    echo "  Windows: dist/wdrive.exe"
    echo "  Linux/Mac: dist/wdrive"
    echo ""
    echo "📋 Build info:"
    ls -lh dist/wdrive*
else
    echo "❌ Build failed!"
    exit 1
fi
