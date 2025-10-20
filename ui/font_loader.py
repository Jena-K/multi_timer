"""
Font loader utility for loading custom fonts.

Version: 1.0.2
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-20

Usage:
    from ui.font_loader import load_fonts

    # Load fonts before creating QApplication
    loaded_fonts = load_fonts()
    print(f"Loaded fonts: {loaded_fonts}")
"""
import sys
from pathlib import Path
from PySide6.QtGui import QFontDatabase


def load_fonts():
    """
    Load custom fonts into the application.

    This function loads Pretendard fonts from the assets/fonts directory.
    Call this function once during application initialization.

    Returns:
        list: List of loaded font family names
    """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        base_path = Path(sys._MEIPASS)
        print(f"[FONT] Running in PyInstaller bundle, base_path: {base_path}")
    else:
        # Running in normal Python environment
        base_path = Path(__file__).parent.parent
        print(f"[FONT] Running in development mode, base_path: {base_path}")

    font_dir = base_path / "assets" / "fonts"
    print(f"[FONT] Font directory: {font_dir}")
    print(f"[FONT] Font directory exists: {font_dir.exists()}")

    fonts_to_load = [
        "Pretendard-Regular.otf",
        "Pretendard-Bold.otf"
    ]

    loaded_fonts = []

    for font_file in fonts_to_load:
        font_path = font_dir / font_file
        print(f"[FONT] Attempting to load: {font_path}")
        print(f"[FONT] File exists: {font_path.exists()}")

        if font_path.exists():
            font_id = QFontDatabase.addApplicationFont(str(font_path))
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                loaded_fonts.extend(font_families)
                print(f"[FONT] ✅ Successfully loaded: {font_file} → {font_families}")
            else:
                print(f"[FONT] ❌ Failed to load font: {font_file}")
        else:
            print(f"[FONT] ⚠️  Font file not found: {font_path}")

    print(f"[FONT] Total loaded fonts: {loaded_fonts}")
    return loaded_fonts
