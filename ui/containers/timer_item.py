"""
Timer item component - manages timer business logic and UI delegation.

Version: 1.0.4
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from datetime import timedelta

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from models.enums import TimerStatus
from models.template import TimerTemplate
from models.timer import TimerInstance
from ui.widgets.timer_list_item import TimerListItem


class TimerItem(QWidget):
    """Timer item with business logic and UI delegation."""

    edit_clicked = Signal(TimerInstance)
    delete_clicked = Signal(TimerInstance)
    timer_completed = Signal(TimerInstance)
    timer_status_changed = Signal(str, bool)  # (template_id, is_running_or_paused)
    timer_clicked = Signal(str)  # (timer_id) - for stopping alert sound

    def __init__(self, timer: TimerInstance, template: TimerTemplate, parent=None):
        """
        Initialize timer item.

        Args:
            timer: TimerInstance to display
            template: Associated TimerTemplate
            parent: Parent widget
        """
        super().__init__(parent)
        self.timer = timer
        self.template = template

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self._on_countdown_tick)

        # Completion blink timer
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._toggle_blink)
        self.blink_state = False

        self._init_ui()
        self._connect_signals()
        self._update_display()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 5)
        layout.setSpacing(0)

        self.list_item = TimerListItem(self.timer, self.template)
        layout.addWidget(self.list_item)

        self.setLayout(layout)

    def _connect_signals(self):
        """Connect UI signals to handlers."""
        self.list_item.edit_clicked.connect(self.edit_clicked.emit)
        self.list_item.delete_clicked.connect(self.delete_clicked.emit)
        self.list_item.start_btn.clicked.connect(self._on_start)
        self.list_item.pause_btn.clicked.connect(self._on_pause)
        self.list_item.stop_btn.clicked.connect(self._on_stop)
        self.list_item.clicked.connect(self._on_timer_clicked)

    def _update_display(self):
        """Update timer display and button states."""
        total_seconds = int(self.timer.remaining_time.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.list_item.update_display(minutes, seconds)
        self.list_item.update_button_states(self.timer.status)

    def _on_start(self):
        """Handle start/resume button click."""
        self.timer.status = TimerStatus.RUNNING
        self.countdown_timer.start(1000)
        self._update_display()
        self.timer_status_changed.emit(str(self.timer.template_id), True)

    def _on_pause(self):
        """Handle pause button click."""
        self.timer.status = TimerStatus.PAUSED
        self.countdown_timer.stop()
        self._update_display()
        self.timer_status_changed.emit(str(self.timer.template_id), True)

    def _on_stop(self):
        """Handle stop button click (reset to template duration)."""
        self.timer.status = TimerStatus.STOPPED
        self.timer.remaining_time = self.template.duration
        self.countdown_timer.stop()
        self._update_display()
        self.timer_status_changed.emit(str(self.timer.template_id), False)

    def _on_countdown_tick(self):
        """Handle countdown timer tick (every 1 second)."""
        if self.timer.status == TimerStatus.RUNNING:
            total_seconds = int(self.timer.remaining_time.total_seconds())

            if total_seconds > 0:
                self.timer.remaining_time = timedelta(seconds=total_seconds - 1)
                self._update_display()
            else:
                self.countdown_timer.stop()
                self.timer.status = TimerStatus.STOPPED
                self.timer.remaining_time = self.template.duration
                self._update_display()
                self.timer_status_changed.emit(str(self.timer.template_id), False)
                self.timer_completed.emit(self.timer)

    def update_timer(self, timer: TimerInstance):
        """
        Update timer data.

        Args:
            timer: Updated timer instance
        """
        self.timer = timer
        self.list_item.update_customer_name(timer.customer_name)
        self._update_display()

    def update_template(self, template: TimerTemplate):
        """
        Update template data and refresh display.

        Args:
            template: Updated template instance
        """
        self.template = template
        self.list_item.update_template_name(template.name)
        # If timer is stopped, update remaining time to new template duration
        if self.timer.status == TimerStatus.STOPPED:
            self.timer.remaining_time = template.duration
            self._update_display()

    def set_highlight(self, highlight: bool):
        """
        Set highlight state for timer completion animation.

        Args:
            highlight: Whether to highlight
        """
        self.list_item.set_highlight(highlight)

    def start_completion_blink(self):
        """Start border blinking animation for timer completion."""
        print(f"[DEBUG] start_completion_blink called for timer {self.timer.id}")
        self.blink_state = False
        self.blink_timer.start(500)  # Blink every 0.5s
        self._toggle_blink()
        print(f"[DEBUG] Blink timer started, initial state: {self.blink_state}")

    def stop_completion_blink(self):
        """Stop border blinking animation."""
        self.blink_timer.stop()
        self.list_item.set_blink_border(False)

    def _toggle_blink(self):
        """Toggle blink state."""
        self.blink_state = not self.blink_state
        print(f"[DEBUG] _toggle_blink: blink_state = {self.blink_state}")
        self.list_item.set_blink_border(self.blink_state)

    def _on_timer_clicked(self):
        """Handle timer item click - stop blinking and sound."""
        self.stop_completion_blink()
        # Notify parent panel to stop alert sound
        self.timer_clicked.emit(str(self.timer.id))
