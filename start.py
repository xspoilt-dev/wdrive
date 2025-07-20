#!/usr/bin/env python3
"""
Simple launcher for wdrive without DNS server
Just starts the Flask server on the local network
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Import and run
    from run import main
    main()
