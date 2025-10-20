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
    # Enable high DPI support on Windows
    from PySide6.QtCore import Qt
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Timer For Ryu")
    app.setOrganizationName("TimerForRyu")

    # Load custom fonts
    load_fonts()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
