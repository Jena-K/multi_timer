"""
Timer For Ryu - Customer Service Timer Manager

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19

Usage:
    uv run python main.py
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.font_loader import load_fonts


def main():
    """Main application entry point."""
    # Enable high DPI support (with compatibility check for older PySide6 versions)
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QFontDatabase

    # Set high DPI attributes BEFORE creating QApplication (critical for Windows)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Enable high DPI scaling for all platforms
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

    app = QApplication(sys.argv)
    app.setApplicationName("Timer For Ryu")
    app.setOrganizationName("TimerForRyu")

    # Load custom fonts first
    loaded_fonts = load_fonts()

    # Set application-wide font rendering for consistency across platforms
    # Try Pretendard first, fallback to system fonts if not available
    font_families = QFontDatabase.families()

    default_font = None
    if "Pretendard" in font_families or "Pretendard" in loaded_fonts:
        default_font = QFont("Pretendard", 11, QFont.Weight.Normal)
    else:
        # Platform-specific fallback fonts
        if sys.platform == "win32":
            default_font = QFont("Malgun Gothic", 11, QFont.Weight.Normal)
        elif sys.platform == "darwin":
            default_font = QFont("SF Pro Text", 11, QFont.Weight.Normal)
        else:
            default_font = QFont("Noto Sans", 11, QFont.Weight.Normal)

    if default_font:
        # Enable font hinting for better cross-platform rendering
        default_font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
        default_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        app.setFont(default_font)

    # Apply platform-specific style sheet for consistent rendering
    platform_stylesheet = """
        * {
            font-family: "Pretendard", "Malgun Gothic", "Microsoft YaHei", "SF Pro Text", system-ui, sans-serif;
        }
    """
    app.setStyleSheet(platform_stylesheet)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
