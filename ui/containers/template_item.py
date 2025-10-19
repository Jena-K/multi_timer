"""
Template item component - manages template business logic and UI delegation.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from models.template import TimerTemplate
from ui.widgets.template_list_item import TemplateListItem


class TemplateItem(QWidget):
    """Template item with business logic and UI delegation."""

    template_clicked = Signal(TimerTemplate)
    edit_clicked = Signal(TimerTemplate)
    delete_clicked = Signal(TimerTemplate)

    def __init__(self, template: TimerTemplate, parent=None):
        """
        Initialize template item.

        Args:
            template: TimerTemplate to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.template = template
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 5)
        layout.setSpacing(0)

        self.list_item = TemplateListItem(self.template)
        self.list_item.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.list_item)

        self.setLayout(layout)

    def _connect_signals(self):
        """Connect UI signals to handlers."""
        self.list_item.edit_clicked.connect(self.edit_clicked.emit)
        self.list_item.delete_clicked.connect(self.delete_clicked.emit)

    def mousePressEvent(self, event):
        """Handle mouse press to emit template clicked signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.template_clicked.emit(self.template)
        super().mousePressEvent(event)

    def update_template(self, template: TimerTemplate):
        """
        Update template data.

        Args:
            template: Updated template instance
        """
        self.template = template
        self.list_item.update_name(template.name)

        total_seconds = int(template.duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.list_item.update_duration(minutes, seconds)

    def set_buttons_enabled(self, enabled: bool):
        """
        Enable or disable edit/delete buttons.

        Args:
            enabled: Whether buttons should be enabled
        """
        self.list_item.set_buttons_enabled(enabled)
