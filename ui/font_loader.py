"""
Font loader utility for loading custom fonts.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19

Usage:
    from ui.font_loader import load_fonts

    # Load fonts before creating QApplication
    load_fonts()
"""
import logging
from PySide6.QtGui import QFontDatabase
from pathlib import Path

logger = logging.getLogger(__name__)


def load_fonts():
    """
    Load custom fonts into the application.

    This function loads Pretendard fonts from the assets/fonts directory.
    Call this function once during application initialization.

    Returns:
        list: List of loaded font family names
    """
    font_dir = Path(__file__).parent.parent / "assets" / "fonts"

    fonts_to_load = [
        "Pretendard-Regular.otf",
        "Pretendard-Bold.otf"
    ]

    loaded_fonts = []

    for font_file in fonts_to_load:
        font_path = font_dir / font_file
        if font_path.exists():
            font_id = QFontDatabase.addApplicationFont(str(font_path))
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                loaded_fonts.extend(font_families)
                logger.info(f"Loaded font: {font_file} → {font_families}")
            else:
                logger.error(f"Failed to load font: {font_file}")
        else:
            logger.warning(f"Font file not found: {font_path}")

    return loaded_fonts
