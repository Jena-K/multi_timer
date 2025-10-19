"""
Windows executable build script for Timer For Ryu.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-20
Last Modified: 2025-10-20

Usage:
    # Install PyInstaller first
    uv pip install pyinstaller

    # Run this script
    uv run python build_windows.py

    # Or use PyInstaller directly
    pyinstaller timer_for_ryu_windows.spec
"""
import subprocess
import sys
from pathlib import Path


def build_windows_exe():
    """Build Windows executable using PyInstaller."""

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Build using spec file
    spec_file = Path(__file__).parent / "timer_for_ryu_windows.spec"

    if not spec_file.exists():
        print(f"Error: {spec_file} not found!")
        print("Please create the spec file first.")
        return False

    print(f"Building Windows executable using {spec_file}...")

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file)
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✅ Build successful!")
        print("Executable location: dist/Timer For Ryu.exe")
    else:
        print("\n❌ Build failed!")
        return False

    return True


if __name__ == "__main__":
    success = build_windows_exe()
    sys.exit(0 if success else 1)
