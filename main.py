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

    # Enable high DPI scaling for all platforms
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

    # Set additional high DPI attributes for better cross-platform compatibility
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Timer For Ryu")
    app.setOrganizationName("TimerForRyu")

    # Load custom fonts first
    load_fonts()

    # Set application-wide font rendering for consistency across platforms
    # Try Pretendard first, fallback to system fonts if not available
    font_families = QFontDatabase.families()
    if "Pretendard" in font_families:
        app.setFont(QFont("Pretendard", 11))
    else:
        # Windows fallback fonts
        if sys.platform == "win32":
            app.setFont(QFont("Malgun Gothic", 11))
        else:
            app.setFont(QFont("system-ui", 11))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
