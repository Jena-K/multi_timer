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
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from ui.font_loader import load_fonts


def exception_hook(exctype, value, tb):
    """Global exception handler for better error reporting."""
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    print(f"\n{'='*60}\nUNHANDLED EXCEPTION:\n{'='*60}\n{error_msg}")

    # Show error dialog if QApplication exists
    if QApplication.instance():
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText("An error occurred:")
        msg_box.setDetailedText(error_msg)
        msg_box.exec()

    sys.__excepthook__(exctype, value, tb)


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
    print(f"\n[MAIN] Loaded custom fonts: {loaded_fonts}")

    # Set application-wide font rendering for consistency across platforms
    # Try Pretendard first, fallback to system fonts if not available
    font_families = QFontDatabase.families()
    print(f"[MAIN] Total system fonts available: {len(font_families)}")

    default_font = None
    if "Pretendard" in font_families or "Pretendard" in loaded_fonts:
        default_font = QFont("Pretendard", 11, QFont.Weight.Normal)
        print("[MAIN] ✅ Using Pretendard font")
    else:
        # Platform-specific fallback fonts
        if sys.platform == "win32":
            default_font = QFont("Malgun Gothic", 11, QFont.Weight.Normal)
            print("[MAIN] ⚠️  Pretendard not found, using Malgun Gothic (Windows)")
        elif sys.platform == "darwin":
            default_font = QFont("SF Pro Text", 11, QFont.Weight.Normal)
            print("[MAIN] ⚠️  Pretendard not found, using SF Pro Text (macOS)")
        else:
            default_font = QFont("Noto Sans", 11, QFont.Weight.Normal)
            print("[MAIN] ⚠️  Pretendard not found, using Noto Sans (Linux)")

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
    # Install global exception handler
    sys.excepthook = exception_hook

    try:
        main()
    except Exception as e:
        print(f"\n{'='*60}\nFATAL ERROR:\n{'='*60}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
