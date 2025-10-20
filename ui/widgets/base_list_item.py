"""
Base list item widget with common functionality.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ui.theme import Theme


class BaseListItem(QFrame):
    """Base class for list item widgets with common button creation."""

    def __init__(self, parent=None):
        """
        Initialize base list item with vertical centering.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._item_height = 0  # Will be set by subclass

        # Set frame properties for dynamic border control
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(0)

    def _create_centered_layout(self) -> QHBoxLayout:
        """
        Create a horizontal layout with fixed padding and vertical alignment.

        Returns:
            QHBoxLayout: Configured layout
        """
        layout = QHBoxLayout()
        # Fixed padding: 8px horizontal, 0px vertical (perfect vertical centering)
        layout.setContentsMargins(Theme.Spacing.MARGIN_MEDIUM, 0, Theme.Spacing.MARGIN_MEDIUM, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        return layout

    def _add_widget_centered(self, layout: QHBoxLayout, widget: QWidget, stretch: int = 0):
        """
        Add a widget to layout with vertical centering.

        Args:
            layout: Target layout
            widget: Widget to add
            stretch: Stretch factor
        """
        layout.addWidget(widget, stretch, Qt.AlignmentFlag.AlignVCenter)

    def _create_label_area(self, label: QLabel) -> QWidget:
        """
        Create a container area with a label inside.
        Container takes full available height for proper centering.

        Args:
            label: QLabel to add to container

        Returns:
            QWidget: Container with label
        """
        container = QWidget()
        # Container takes full item height (no vertical margins)
        container.setFixedHeight(self._item_height)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(label, 0, Qt.AlignmentFlag.AlignVCenter)
        return container

    def _create_action_buttons_area(self, edit_btn: QPushButton, delete_btn: QPushButton) -> QWidget:
        """
        Create action buttons area with two vertical sections (area4_1 and area4_2).

        Args:
            edit_btn: Edit button (placed in area4_1)
            delete_btn: Delete button (placed in area4_2)

        Returns:
            QWidget: Container with two vertical areas containing buttons
        """
        # area4 - Main container (same height as other areas for consistent vertical alignment)
        area4 = QWidget()
        # Container takes full item height (no vertical margins)
        area4.setFixedHeight(self._item_height)

        layout = QVBoxLayout(area4)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # area4_1 - Top area for edit button (fixed 20px height)
        area4_1 = QWidget()
        area4_1.setFixedHeight(20)
        area4_1_layout = QHBoxLayout(area4_1)
        area4_1_layout.setContentsMargins(0, 0, 0, 0)
        area4_1_layout.setSpacing(0)
        area4_1_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        area4_1_layout.addStretch()
        area4_1_layout.addWidget(edit_btn, 0, Qt.AlignmentFlag.AlignVCenter)

        # area4_2 - Bottom area for delete button (fixed 20px height)
        area4_2 = QWidget()
        area4_2.setFixedHeight(20)
        area4_2_layout = QHBoxLayout(area4_2)
        area4_2_layout.setContentsMargins(0, 0, 0, 0)
        area4_2_layout.setSpacing(0)
        area4_2_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        area4_2_layout.addStretch()
        area4_2_layout.addWidget(delete_btn, 0, Qt.AlignmentFlag.AlignVCenter)

        # Add both areas to main layout with stretch for vertical centering
        layout.addStretch()
        layout.addWidget(area4_1, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(area4_2, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addStretch()

        return area4

    def _create_action_button(self, text: str) -> QPushButton:
        """
        Create an action button (Edit/Delete) with fixed height.

        Args:
            text: Button text

        Returns:
            QPushButton: Configured action button
        """
        btn = QPushButton(text)
        # Fixed button height: 20px
        # Button width: 55% of item height - 2px
        button_width = 27
        button_height = 21

        btn.setMinimumSize(button_width, button_height)
        btn.setMaximumSize(button_width, button_height)
        btn.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_SMALL))
        btn.setFlat(True)  # Remove default button styling on Windows
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.Colors.TEXT_TERTIARY};
                color: {Theme.Colors.WHITE};
                border: none;
                border-radius: {Theme.Spacing.RADIUS_SMALL}px;
                padding: 2px;
                margin: 1px;
                text-align: center;
                font-family: {Theme.Fonts.FAMILY_FALLBACK};
            }}
            QPushButton:hover {{
                background-color: {Theme.Colors.TEXT_SECONDARY};
            }}
            QPushButton:pressed {{
                background-color: #616161;
            }}
            QPushButton:disabled {{
                background-color: {Theme.Colors.BORDER};
                color: {Theme.Colors.TEXT_TERTIARY};
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        return btn


def format_duration(minutes: int, seconds: int) -> str:
    """
    Format duration as Korean string.

    Args:
        minutes: Minutes value
        seconds: Seconds value

    Returns:
        str: Formatted duration (e.g., "05 분 30 초")
    """
    return f"{minutes:02d} 분 {seconds:02d} 초"


def format_time_display(minutes: int, seconds: int) -> str:
    """
    Format time for timer display.

    Args:
        minutes: Minutes value
        seconds: Seconds value

    Returns:
        str: Formatted time (e.g., "05 : 30")
    """
    return f"{minutes:02d} : {seconds:02d}"
