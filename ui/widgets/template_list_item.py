"""
Template list item component - separates item layout from business logic.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from models.template import TimerTemplate
from ui.theme import Theme
from ui.widgets.base_list_item import BaseListItem, format_duration


class TemplateListItem(BaseListItem):
    """Single template list item with 3-area layout."""

    edit_clicked = Signal(TimerTemplate)
    delete_clicked = Signal(TimerTemplate)

    def __init__(self, template: TimerTemplate, parent=None):
        super().__init__(parent)
        self.template = template
        self._item_height = Theme.Spacing.TEMPLATE_ITEM_HEIGHT
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setFixedHeight(self._item_height)

        main_layout = self._create_centered_layout()

        # Area 1: Template name (50%, left aligned)
        name_area = self._create_name_area()
        self._add_widget_centered(main_layout, name_area, 50)

        # Area 2: Duration (30%, center aligned)
        duration_area = self._create_duration_area()
        self._add_widget_centered(main_layout, duration_area, 30)

        # Area 3: Edit/Delete buttons (20%, right aligned)
        buttons_area = self._create_buttons_area()
        self._add_widget_centered(main_layout, buttons_area, 20)

        self.setLayout(main_layout)
        self.setLineWidth(2)
        self.setStyleSheet(f"""
            TemplateListItem {{
                background-color: {Theme.Colors.PANEL_BACKGROUND};
                border: 2px solid {Theme.Colors.BORDER};
                border-radius: {Theme.Spacing.RADIUS_LARGE}px;
            }}
            TemplateListItem:hover {{
                background-color: {Theme.Colors.BACKGROUND};
            }}
            QWidget {{
                background-color: transparent;
            }}
            QLabel {{
                background-color: transparent;
            }}
        """)

    def _create_name_area(self) -> QWidget:
        """Create Area 1: Template name."""
        self.name_label = QLabel(self.template.name)
        self.name_label.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_LARGE))
        self.name_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.name_label.setContentsMargins(0, 0, 0, 0)
        return self._create_label_area(self.name_label)

    def _create_duration_area(self) -> QWidget:
        """Create Area 2: Duration display."""
        total_seconds = int(self.template.duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        self.duration_label = QLabel(format_duration(minutes, seconds))
        self.duration_label.setFont(Theme.Fonts.item_name())
        self.duration_label.setStyleSheet(f"color: {Theme.Colors.TEXT_SECONDARY};")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.duration_label.setContentsMargins(0, 0, 0, 0)
        return self._create_label_area(self.duration_label)

    def _create_buttons_area(self) -> QWidget:
        """Create Area 3: Edit/Delete buttons."""
        self.edit_btn = self._create_action_button("수정")
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.template))

        self.delete_btn = self._create_action_button("삭제")
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.template))

        return self._create_action_buttons_area(self.edit_btn, self.delete_btn)

    def update_name(self, name: str):
        """Update template name display."""
        self.name_label.setText(name)

    def update_duration(self, minutes: int, seconds: int):
        """Update duration display."""
        self.duration_label.setText(format_duration(minutes, seconds))

    def set_buttons_enabled(self, enabled: bool):
        """
        Enable or disable edit/delete buttons.

        Args:
            enabled: Whether buttons should be enabled
        """
        self.edit_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
