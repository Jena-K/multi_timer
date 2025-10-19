"""
Base panel class with common functionality.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PySide6.QtCore import Signal
from typing import List, Generic, TypeVar
from ui.theme import Theme

T = TypeVar('T')  # Widget type (TemplateItem or TimerItem)


class BaseListPanel(QWidget, Generic[T]):
    """Base class for list-based panels with drag & drop support."""

    items_reordered = Signal(list)

    def __init__(self, parent=None):
        """Initialize base panel."""
        super().__init__(parent)
        self.items: List[T] = []

    def _create_header(self, title: str) -> QLabel:
        """
        Create panel header label.

        Args:
            title: Header text

        Returns:
            QLabel: Configured header label
        """
        header = QLabel(title)
        header.setFont(Theme.Fonts.header())
        header.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        return header

    def _create_list_widget(self) -> QListWidget:
        """
        Create configured list widget with drag & drop.

        Returns:
            QListWidget: Configured list widget
        """
        list_widget = QListWidget()
        list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        list_widget.setSpacing(0)
        list_widget.setStyleSheet(Theme.Styles.list_widget())
        list_widget.model().rowsMoved.connect(self._on_rows_moved)
        return list_widget

    def _create_main_layout(self) -> QVBoxLayout:
        """
        Create main layout with standard margins and spacing.

        Returns:
            QVBoxLayout: Configured layout
        """
        layout = QVBoxLayout()
        layout.setContentsMargins(
            Theme.Spacing.PADDING_XLARGE,
            Theme.Spacing.PADDING_XLARGE,
            Theme.Spacing.PADDING_XLARGE,
            Theme.Spacing.PADDING_XLARGE
        )
        layout.setSpacing(Theme.Spacing.MARGIN_MEDIUM)
        return layout

    def add_item_to_list(self, item_widget: T):
        """
        Add item widget to list.

        Args:
            item_widget: Widget to add
        """
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.list_widget.insertItem(0, item)
        self.list_widget.setItemWidget(item, item_widget)
        self.items.insert(0, item_widget)

    def remove_item_by_id(self, item_id: str, id_getter) -> bool:
        """
        Remove item by ID.

        Args:
            item_id: ID to match
            id_getter: Function to extract ID from item widget

        Returns:
            bool: True if item was found and removed
        """
        for i, item_widget in enumerate(self.items):
            if str(id_getter(item_widget)) == item_id:
                item = self.list_widget.takeItem(i)
                del item
                self.items.pop(i)
                return True
        return False

    def find_item_by_id(self, item_id, id_getter) -> T:
        """
        Find item by ID.

        Args:
            item_id: ID to match
            id_getter: Function to extract ID from item widget

        Returns:
            T: Found item widget or None
        """
        for item_widget in self.items:
            if id_getter(item_widget) == item_id:
                return item_widget
        return None

    def clear_items(self):
        """Clear all items from list."""
        self.list_widget.clear()
        self.items.clear()

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
        # Rebuild items list from current widget order
        self.items.clear()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if widget:
                self.items.append(widget)

        # Emit reordered signal with underlying data
        self._emit_reordered()

    def _emit_reordered(self):
        """
        Emit reordered signal.
        Override this method to customize what data is emitted.
        """
        raise NotImplementedError("Subclasses must implement _emit_reordered")
