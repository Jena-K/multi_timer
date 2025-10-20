"""
Timer panel (right panel) for active timers.

Version: 1.0.2
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from pathlib import Path
from typing import List

from PySide6.QtCore import QTimer, QUrl, Signal
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from models.enums import TimerStatus
from models.template import TimerTemplate
from models.timer import TimerInstance
from ui.containers.timer_item import TimerItem
from ui.theme import Theme


class TimerPanel(QWidget):
    """Right panel for active timer management."""

    # Alert sound constants
    ALERT_BEEP_COUNT = 10  # Number of beeps
    ALERT_BEEP_INTERVAL = 500  # Milliseconds between beeps
    ALERT_VOLUME = 0.7  # Volume level (0.0 - 1.0)
    SOUND_FILE = "alert.wav"  # Alert sound filename

    edit_timer_clicked = Signal(TimerInstance)
    delete_timer_clicked = Signal(TimerInstance)
    timer_completed = Signal(TimerInstance)
    timers_reordered = Signal(list)
    template_button_update_needed = Signal(str, bool)  # (template_id, has_running_timers)

    def __init__(self, parent=None):
        """Initialize timer panel."""
        super().__init__(parent)
        self.timer_items: List[TimerItem] = []

        # Initialize sound effect
        self.sound_effect = self._init_sound_effect()

        # Alert repeat control
        self.alert_timer = QTimer()
        self.alert_timer.timeout.connect(self._play_alert_beep)
        self.alert_count = 0

        self._init_ui()

    def _init_sound_effect(self) -> QSoundEffect:
        """
        Initialize alert sound effect.

        Returns:
            QSoundEffect: Configured sound effect
        """
        sound_effect = QSoundEffect()
        sound_path = Path(__file__).parent.parent.parent / "assets" / self.SOUND_FILE
        if sound_path.exists():
            sound_effect.setSource(QUrl.fromLocalFile(str(sound_path)))
            sound_effect.setVolume(self.ALERT_VOLUME)
        return sound_effect

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
        header = QLabel("타이머")
        header.setFont(Theme.Fonts.header())
        header.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        layout.addWidget(header)

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
            TimerPanel {{
                background-color: transparent;
            }}
        """)

    def set_timers(self, timers_with_templates: List[tuple[TimerInstance, TimerTemplate]]):
        """
        Display list of timers.

        Args:
            timers_with_templates: List of (timer, template) tuples
        """
        self.clear_timers()
        for timer, template in timers_with_templates:
            self.add_timer_item(timer, template, emit_signal=False)

    def add_timer_item(
        self,
        timer: TimerInstance,
        template: TimerTemplate,
        emit_signal: bool = True
    ):
        """
        Add a timer item to the list.

        Args:
            timer: TimerInstance to add
            template: Associated template
            emit_signal: Whether to emit signals
        """
        item_widget = TimerItem(timer, template)
        item_widget.edit_clicked.connect(self.edit_timer_clicked.emit)
        item_widget.delete_clicked.connect(self.delete_timer_clicked.emit)
        item_widget.timer_completed.connect(self._on_timer_completed)
        item_widget.timer_status_changed.connect(self._on_timer_status_changed)
        item_widget.timer_clicked.connect(self._on_timer_item_clicked)

        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.list_widget.addItem(item)  # Add to bottom instead of top
        self.list_widget.setItemWidget(item, item_widget)
        self.timer_items.append(item_widget)  # Append instead of insert(0)

    def remove_timer_item(self, timer_id: str):
        """
        Remove timer item by ID.

        Args:
            timer_id: UUID string of timer to remove
        """
        for i, item_widget in enumerate(self.timer_items):
            if str(item_widget.timer.id) == timer_id:
                item = self.list_widget.takeItem(i)
                del item
                self.timer_items.pop(i)
                break

    def update_timer_item(self, timer: TimerInstance):
        """
        Update existing timer item.

        Args:
            timer: Updated timer instance
        """
        for item_widget in self.timer_items:
            if item_widget.timer.id == timer.id:
                item_widget.update_timer(timer)
                break

    def update_timers_by_template(self, template: TimerTemplate):
        """
        Update all timer items that use this template.

        Args:
            template: Updated template instance
        """
        for item_widget in self.timer_items:
            if item_widget.timer.template_id == template.id:
                item_widget.update_template(template)

    def clear_timers(self):
        """Clear all timer items."""
        self.list_widget.clear()
        self.timer_items.clear()

    def _play_alert_beep(self):
        """Play one beep in the alert sequence."""
        self.sound_effect.play()
        self.alert_count += 1
        if self.alert_count >= self.ALERT_BEEP_COUNT:
            self.alert_timer.stop()
            self.alert_count = 0

    def _on_timer_completed(self, timer: TimerInstance):
        """
        Handle timer completion.

        Args:
            timer: Completed timer instance
        """
        for item_widget in self.timer_items:
            if item_widget.timer.id == timer.id:
                # Start border blinking animation (continues until clicked)
                item_widget.start_completion_blink()

                # Start repeating beep pattern
                self.alert_count = 0
                self.sound_effect.play()  # First beep immediately
                self.alert_count = 1
                self.alert_timer.start(self.ALERT_BEEP_INTERVAL)

                break

        self.timer_completed.emit(timer)

    def get_timer_item(self, timer_id: str) -> TimerItem:
        """
        Get timer item by timer ID.

        Args:
            timer_id: UUID string

        Returns:
            TimerItem or None
        """
        for item_widget in self.timer_items:
            if str(item_widget.timer.id) == timer_id:
                return item_widget
        return None

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
        self.timer_items.clear()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if isinstance(widget, TimerItem):
                self.timer_items.append(widget)

        timers = [item_widget.timer for item_widget in self.timer_items]
        self.timers_reordered.emit(timers)

    def _on_timer_status_changed(self, template_id: str, is_running: bool):
        """
        Handle timer status change.

        Args:
            template_id: Template ID of the timer
            is_running: Whether the timer is running or paused
        """
        # Check if any timer using this template is running or paused
        has_running_timers = False
        for item_widget in self.timer_items:
            if str(item_widget.timer.template_id) == template_id:
                if item_widget.timer.status in [TimerStatus.RUNNING, TimerStatus.PAUSED]:
                    has_running_timers = True
                    break

        # Emit signal to update template buttons
        self.template_button_update_needed.emit(template_id, has_running_timers)

    def _on_timer_item_clicked(self, timer_id: str):
        """
        Handle timer item click - stop alert sound if playing.

        Args:
            timer_id: ID of clicked timer
        """
        # Stop alert sound and timer
        if self.alert_timer.isActive():
            self.alert_timer.stop()
            self.alert_count = 0
