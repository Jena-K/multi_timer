"""
Template management panel (left panel).

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from typing import List

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget

from models.template import TimerTemplate
from ui.containers.template_item import TemplateItem
from ui.theme import Theme


class TemplatePanel(QWidget):
    """Left panel for template management."""

    add_template_clicked = Signal()
    template_selected = Signal(TimerTemplate)
    edit_template_clicked = Signal(TimerTemplate)
    delete_template_clicked = Signal(TimerTemplate)
    templates_reordered = Signal(list)

    def __init__(self, parent=None):
        """Initialize template panel."""
        super().__init__(parent)
        self.template_items: List[TemplateItem] = []
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.Spacing.PADDING_XLARGE,
            Theme.Spacing.PADDING_XLARGE,
            Theme.Spacing.PADDING_XLARGE,
            Theme.Spacing.PADDING_XLARGE
        )
        layout.setSpacing(Theme.Spacing.MARGIN_MEDIUM)

        # Header label
        header = QLabel("타이머 템플릿")
        header.setFont(Theme.Fonts.header())
        header.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        layout.addWidget(header)

        # Add Template button
        add_btn = QPushButton("+ 템플릿 추가")
        add_btn.setFixedHeight(Theme.Spacing.BUTTON_HEIGHT)
        add_btn.setFont(Theme.Fonts.button())
        add_btn.setStyleSheet(Theme.Styles.primary_button())
        add_btn.clicked.connect(self.add_template_clicked.emit)
        layout.addWidget(add_btn)

        # List widget with drag & drop support
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.setSpacing(0)
        self.list_widget.setStyleSheet(Theme.Styles.list_widget())
        self.list_widget.model().rowsMoved.connect(self._on_rows_moved)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        # Panel styling with background
        self.setStyleSheet(f"""
            TemplatePanel {{
                background-color: transparent;
                border-right: 1px solid {Theme.Colors.BORDER};
            }}
        """)

    def set_templates(self, templates: List[TimerTemplate]):
        """
        Display list of templates.

        Args:
            templates: List of TimerTemplate instances
        """
        self.clear_templates()
        for template in templates:
            self.add_template_item(template, emit_signal=False)

    def add_template_item(self, template: TimerTemplate, emit_signal: bool = True):
        """
        Add a template item to the list.

        Args:
            template: TimerTemplate to add
            emit_signal: Whether to emit signals (False when loading from DB)
        """
        item_widget = TemplateItem(template)
        item_widget.template_clicked.connect(self.template_selected.emit)
        item_widget.edit_clicked.connect(self.edit_template_clicked.emit)
        item_widget.delete_clicked.connect(self.delete_template_clicked.emit)

        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.list_widget.insertItem(0, item)
        self.list_widget.setItemWidget(item, item_widget)
        self.template_items.insert(0, item_widget)

    def remove_template_item(self, template_id: str):
        """
        Remove template item by ID.

        Args:
            template_id: UUID string of template to remove
        """
        for i, item_widget in enumerate(self.template_items):
            if str(item_widget.template.id) == template_id:
                item = self.list_widget.takeItem(i)
                del item
                self.template_items.pop(i)
                break

    def update_template_item(self, template: TimerTemplate):
        """
        Update existing template item.

        Args:
            template: Updated template instance
        """
        for item_widget in self.template_items:
            if item_widget.template.id == template.id:
                item_widget.update_template(template)
                break

    def clear_templates(self):
        """Clear all template items."""
        self.list_widget.clear()
        self.template_items.clear()

    def _on_rows_moved(self, parent, start, end, destination, row):
        """
        Handle drag & drop reordering.

        Args:
            parent: Parent index
            start: Start row
            end: End row
            destination: Destination index
            row: Target row
        """
        self.template_items.clear()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if isinstance(widget, TemplateItem):
                self.template_items.append(widget)

        templates = [item_widget.template for item_widget in self.template_items]
        self.templates_reordered.emit(templates)

    def update_template_buttons(self, template_id: str, has_running_timers: bool):
        """
        Update template item buttons based on child timer states.

        Args:
            template_id: UUID string of template
            has_running_timers: Whether this template has any running/paused timers
        """
        for item_widget in self.template_items:
            if str(item_widget.template.id) == template_id:
                item_widget.set_buttons_enabled(not has_running_timers)
                break
