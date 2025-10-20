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

    # Enable high DPI scaling for all platforms
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy')
        else Qt.AA_EnableHighDpiScaling
    )

    # Set additional high DPI attributes for better cross-platform compatibility
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Timer For Ryu")
    app.setOrganizationName("TimerForRyu")

    # Set application-wide font rendering for consistency across platforms
    from PySide6.QtGui import QFont
    app.setFont(QFont("Pretendard", 11))

    # Load custom fonts
    load_fonts()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
