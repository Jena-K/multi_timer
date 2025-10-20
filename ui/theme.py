"""
Centralized design system theme configuration.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19

Usage:
    from ui.theme import Theme

    # Use color constants
    button.setStyleSheet(f"background-color: {Theme.Colors.PRIMARY};")

    # Use font configurations
    label.setFont(Theme.Fonts.header())
"""
from PySide6.QtGui import QFont


class Theme:
    """Centralized theme configuration for Timer For Ryu application."""

    class Colors:
        """Color palette."""
        # Primary colors
        PRIMARY = "#27ae60"
        PRIMARY_HOVER = "#229954"
        PRIMARY_PRESSED = "#1e8449"

        # Neutral colors
        WHITE = "#ffffff"
        BACKGROUND = "#f5f5f5"
        PANEL_BACKGROUND = "#fafafa"
        TEXT_PRIMARY = "#424242"
        TEXT_SECONDARY = "#757575"

        # Border colors
        BORDER = "#e0e0e0"
        BORDER_HOVER = "#bdbdbd"
        BORDER_FOCUS = "#27ae60"

        # Status colors
        SUCCESS = "#27ae60"
        WARNING = "#f39c12"
        ERROR = "#e74c3c"
        DANGER = "#e74c3c"
        DANGER_HOVER = "#c0392b"
        INFO = "#3498db"

        # Text colors
        TEXT_TERTIARY = "#9e9e9e"

        # Timer completion alert (blink animation)
        COMPLETION_BORDER = "#8bc34a"  # Light green border
        COMPLETION_BACKGROUND = "#f1f8e9"  # Very light green background

        # Toast notification
        TOAST_BACKGROUND = "rgba(66, 66, 66, 220)"  # Semi-transparent dark background
        TOAST_TEXT = "#ffffff"  # White text

    class Fonts:
        """Font configurations."""
        FAMILY = "Pretendard"
        FAMILY_FALLBACK = "Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif"

        # Font sizes
        SIZE_SMALL = 10
        SIZE_NORMAL = 11
        SIZE_MEDIUM = 12
        SIZE_LARGE = 13
        SIZE_XLARGE = 14
        SIZE_TIMER = 20
        SIZE_CONTROL_BUTTON = 28

        # Input font size (slightly smaller than label for better fit)
        SIZE_INPUT = 11

        @staticmethod
        def regular(size: int = SIZE_NORMAL) -> QFont:
            """
            Create regular weight font.

            Args:
                size: Font size in pixels

            Returns:
                QFont: Regular font
            """
            return QFont(Theme.Fonts.FAMILY, size, QFont.Weight.Normal)

        @staticmethod
        def bold(size: int = SIZE_NORMAL) -> QFont:
            """
            Create bold weight font.

            Args:
                size: Font size in pixels

            Returns:
                QFont: Bold font
            """
            return QFont(Theme.Fonts.FAMILY, size, QFont.Weight.Bold)

        @staticmethod
        def header() -> QFont:
            """Panel header font (12px, bold)."""
            return Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM)

        @staticmethod
        def button() -> QFont:
            """Button font (14px, bold)."""
            return Theme.Fonts.bold(Theme.Fonts.SIZE_XLARGE)

        @staticmethod
        def label() -> QFont:
            """Standard label font (12px, regular)."""
            return Theme.Fonts.regular(Theme.Fonts.SIZE_MEDIUM)

        @staticmethod
        def input() -> QFont:
            """Input field font (11px, regular)."""
            return Theme.Fonts.regular(Theme.Fonts.SIZE_INPUT)

        @staticmethod
        def timer_display() -> QFont:
            """Timer display font (24px, regular)."""
            return Theme.Fonts.regular(Theme.Fonts.SIZE_TIMER)

        @staticmethod
        def item_name() -> QFont:
            """Item name font (13px, regular)."""
            return Theme.Fonts.regular(Theme.Fonts.SIZE_LARGE)

        @staticmethod
        def item_info() -> QFont:
            """Item info font (11px, regular)."""
            return Theme.Fonts.regular(Theme.Fonts.SIZE_NORMAL)

    class Spacing:
        """Spacing and sizing constants."""
        # Padding
        PADDING_SMALL = 4
        PADDING_MEDIUM = 8
        PADDING_LARGE = 12
        PADDING_XLARGE = 16

        # Margins
        MARGIN_SMALL = 4
        MARGIN_MEDIUM = 8
        MARGIN_LARGE = 12
        MARGIN_XLARGE = 16

        # Border radius
        RADIUS_SMALL = 4
        RADIUS_MEDIUM = 6
        RADIUS_LARGE = 8

        # Item heights
        BUTTON_HEIGHT = 40
        INPUT_HEIGHT = 32
        TIMER_ITEM_HEIGHT = 70
        TEMPLATE_ITEM_HEIGHT = 70

        # Button sizes
        CONTROL_BUTTON_SIZE = 42

        # Input widths
        INPUT_WIDTH_SMALL = 50
        INPUT_WIDTH_MEDIUM = 80
        INPUT_WIDTH_LARGE = 200

    class Styles:
        """Pre-built stylesheet strings."""

        @staticmethod
        def primary_button() -> str:
            """Primary action button style."""
            return f"""
                QPushButton {{
                    background-color: {Theme.Colors.PRIMARY};
                    color: {Theme.Colors.WHITE};
                    border: none;
                    border-radius: {Theme.Spacing.RADIUS_MEDIUM}px;
                    font-family: "{Theme.Fonts.FAMILY}";
                    font-size: {Theme.Fonts.SIZE_XLARGE}px;
                    font-weight: bold;
                    padding: {Theme.Spacing.PADDING_MEDIUM}px {Theme.Spacing.PADDING_LARGE}px;
                }}
                QPushButton:hover {{
                    background-color: {Theme.Colors.PRIMARY_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {Theme.Colors.PRIMARY_PRESSED};
                }}
            """

        @staticmethod
        def secondary_button() -> str:
            """Secondary action button style."""
            return f"""
                QPushButton {{
                    background-color: {Theme.Colors.PANEL_BACKGROUND};
                    color: {Theme.Colors.TEXT_PRIMARY};
                    border: 1px solid {Theme.Colors.BORDER};
                    border-radius: {Theme.Spacing.RADIUS_SMALL}px;
                    font-family: "{Theme.Fonts.FAMILY}";
                    font-size: {Theme.Fonts.SIZE_NORMAL}px;
                    padding: {Theme.Spacing.PADDING_SMALL}px {Theme.Spacing.PADDING_MEDIUM}px;
                }}
                QPushButton:hover {{
                    background-color: {Theme.Colors.BACKGROUND};
                    border-color: {Theme.Colors.BORDER_HOVER};
                }}
            """

        @staticmethod
        def input_field() -> str:
            """Standard input field style."""
            return f"""
                QLineEdit {{
                    border: 1px solid {Theme.Colors.BORDER};
                    border-radius: {Theme.Spacing.RADIUS_SMALL}px;
                    padding: {Theme.Spacing.PADDING_SMALL}px {Theme.Spacing.PADDING_MEDIUM}px;
                    font-family: "{Theme.Fonts.FAMILY}";
                    font-size: {Theme.Fonts.SIZE_INPUT}px;
                    background-color: {Theme.Colors.WHITE};
                }}
                QLineEdit:focus {{
                    border-color: {Theme.Colors.BORDER_FOCUS};
                }}
            """

        @staticmethod
        def list_widget() -> str:
            """List widget style."""
            return f"""
                QListWidget {{
                    border: none;
                    background-color: {Theme.Colors.PANEL_BACKGROUND};
                    outline: none;
                }}
                QListWidget::item {{
                    border: none;
                    background-color: transparent;
                }}
                QListWidget::item:selected {{
                    background-color: transparent;
                    border: none;
                }}
            """

        @staticmethod
        def dialog() -> str:
            """Dialog window style."""
            return f"""
                QDialog {{
                    background-color: {Theme.Colors.WHITE};
                }}
            """

        @staticmethod
        def panel() -> str:
            """Panel container style."""
            return f"""
                QWidget {{
                    background-color: {Theme.Colors.WHITE};
                }}
            """

        @staticmethod
        def main_window() -> str:
            """Main window style."""
            return f"""
                QMainWindow {{
                    background-color: {Theme.Colors.PANEL_BACKGROUND};
                }}
                QSplitter::handle {{
                    background-color: {Theme.Colors.BORDER};
                    width: 2px;
                }}
                QWidget {{
                    background-color: {Theme.Colors.WHITE};
                }}
            """

        @staticmethod
        def message_box(danger_text: str = "삭제", cancel_text: str = "취소") -> str:
            """
            Message box style.

            Args:
                danger_text: Text for danger button (default: "삭제")
                cancel_text: Text for cancel button (default: "취소")

            Returns:
                str: Stylesheet for message box
            """
            return f"""
                QMessageBox {{
                    background-color: {Theme.Colors.WHITE};
                }}
                QLabel {{
                    color: {Theme.Colors.TEXT_PRIMARY};
                    font-family: "{Theme.Fonts.FAMILY}";
                    font-size: {Theme.Fonts.SIZE_NORMAL}px;
                }}
                QPushButton {{
                    min-width: 80px;
                    min-height: 30px;
                    border: none;
                    border-radius: {Theme.Spacing.RADIUS_SMALL}px;
                    font-family: "{Theme.Fonts.FAMILY}";
                    font-size: {Theme.Fonts.SIZE_MEDIUM}px;
                    padding: 5px 15px;
                }}
                QPushButton[text="{danger_text}"] {{
                    background-color: {Theme.Colors.DANGER};
                    color: {Theme.Colors.WHITE};
                    font-weight: bold;
                }}
                QPushButton[text="{danger_text}"]:hover {{
                    background-color: {Theme.Colors.DANGER_HOVER};
                }}
                QPushButton[text="{cancel_text}"] {{
                    background-color: #95a5a6;
                    color: {Theme.Colors.WHITE};
                }}
                QPushButton[text="{cancel_text}"]:hover {{
                    background-color: #7f8c8d;
                }}
            """
