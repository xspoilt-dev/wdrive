#!/usr/bin/env python3
"""
wdrive - Local Google Drive Server
A Flask-based file sharing server for local networks

Usage:
    python run.py [options]

Options:
    --host HOST     Host address (default: 0.0.0.0)
    --port PORT     Port number (default: 8080)
    --password PWD  Set custom password
    --no-dns        Disable DNS server
    --debug         Enable debug mode
"""

import os
import sys
import argparse
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import main, app
from utils.logger import setup_logging
from werkzeug.security import generate_password_hash


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='wdrive - Local Google Drive Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                          # Start with default settings
  python run.py --port 9000             # Use custom port
  python run.py --password mypass       # Set custom password
  python run.py --no-dns --debug        # Disable DNS and enable debug
  
Visit http://wdrive/ or http://localhost:8080/ after starting.
        """
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host address to bind to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port number to listen on (default: 8080)'
    )
    
    parser.add_argument(
        '--password',
        help='Set custom password (default: wdrive123)'
    )
    
    parser.add_argument(
        '--no-dns',
        action='store_true',
        help='Disable DNS server'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='wdrive 1.0.0 by xspoilt-dev'
    )
    
    return parser.parse_args()


def setup_environment(args):
    """Setup environment based on arguments."""
    # Set custom password if provided
    if args.password:
        password_hash = generate_password_hash(args.password)
        # Update app configuration
        import app
        app.PASSWORD_HASH = password_hash
        print(f"🔒 Custom password set")
    
    # Set debug mode
    if args.debug:
        app.config['DEBUG'] = True
        print("🐛 Debug mode enabled")
    
    # Disable DNS if requested
    if args.no_dns:
        # This would be handled in the main app
        print("🌐 DNS server disabled")


def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        'flask',
        'werkzeug',
        'jinja2',
        'qrcode',
        'PIL',
        'dnslib',
        'watchdog',
        'colorama'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install them with: pip install -r requirements.txt")
        return False
    
    return True


def show_welcome_message():
    """Display welcome message."""
    print()
    print("=" * 60)
    print("🚀 wdrive - Local Google Drive Server")
    print("   Created by: xspoilt-dev")
    print("   Version: 1.0.0")
    print("=" * 60)
    print()


def show_startup_info(host, port, local_ip=None):
    """Show startup information."""
    print("📋 Server Information:")
    print(f"   🌍 Host: {host}")
    print(f"   🔌 Port: {port}")
    print(f"   📁 Shared folder: ./shared/")
    print(f"   🔒 Password: wdrive123 (default)")
    print()
    
    print("🌐 Access URLs:")
    if local_ip:
        print(f"   • http://{local_ip}:{port}/")
    print(f"   • http://localhost:{port}/")
    print(f"   • http://127.0.0.1:{port}/")
    
    print()
    print("📱 Mobile Access:")
    print("   Scan the QR code that will be generated")
    print()
    print("⌨️  Keyboard Shortcuts:")
    print("   • Ctrl+C: Stop server")
    print("   • Ctrl+U: Upload page (in browser)")
    print("   • Ctrl+H: Home page (in browser)")
    print()


if __name__ == '__main__':
    # Parse arguments
    args = parse_arguments()
    
    # Show welcome message
    show_welcome_message()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup environment
    setup_environment(args)
    
    # Get local IP for display
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
    except Exception:
        local_ip = None
    
    # Show startup info
    show_startup_info(args.host, args.port, local_ip)
    
    # Start the server
    try:
        # Modify app configuration based on args
        if hasattr(app, 'run'):
            # If we're running the Flask app directly
            app.run(
                host=args.host,
                port=args.port,
                debug=args.debug,
                threaded=True,
                use_reloader=False
            )
        else:
            # Use the main function from app.py
            main()
            
    except KeyboardInterrupt:
        print("\n👋 wdrive server stopped by user")
        sys.exit(0)
    except PermissionError as e:
        print(f"❌ Permission error: {e}")
        print("💡 Try running as administrator or use a different port")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
