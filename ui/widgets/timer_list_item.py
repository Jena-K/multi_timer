"""
Timer list item component - separates item layout from widget container.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from models.enums import TimerStatus
from models.template import TimerTemplate
from models.timer import TimerInstance
from ui.theme import Theme
from ui.widgets.base_list_item import BaseListItem, format_time_display


class TimerListItem(BaseListItem):
    """Single timer list item with 4-area layout."""

    edit_clicked = Signal(TimerInstance)
    delete_clicked = Signal(TimerInstance)
    clicked = Signal()

    def __init__(self, timer: TimerInstance, template: TimerTemplate, parent=None):
        super().__init__(parent)
        self.timer = timer
        self.template = template
        self._item_height = Theme.Spacing.TIMER_ITEM_HEIGHT
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setFixedHeight(self._item_height)

        main_layout = self._create_centered_layout()

        # Area 1: Template + Customer name (0-20%, left aligned)
        area1 = self._create_info_area()
        self._add_widget_centered(main_layout, area1, 20)

        # Area 2: Control buttons (20-55%, center aligned)
        area2 = self._create_controls_area()
        self._add_widget_centered(main_layout, area2, 35)

        # Area 3: Time display (55-90%, center aligned)
        area3 = self._create_time_area()
        self._add_widget_centered(main_layout, area3, 35)

        # Area 4: Edit/Delete buttons (90-100%, right aligned)
        area4 = self._create_actions_area()
        self._add_widget_centered(main_layout, area4, 10)

        self.setLayout(main_layout)

        # Set initial normal state style with visible border
        self.setLineWidth(2)
        self.setStyleSheet(f"""
            TimerListItem {{
                background-color: {Theme.Colors.PANEL_BACKGROUND};
                border: 2px solid {Theme.Colors.BORDER};
                border-radius: {Theme.Spacing.RADIUS_LARGE}px;
            }}
        """)

    def _create_info_area(self) -> QWidget:
        """Create Area 1: Template name (1-1) + Customer name (1-2) stacked vertically."""
        container = QWidget()
        container.setFixedHeight(self._item_height)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Area 1-1: Customer name (larger, bold, primary)
        self.customer_label = QLabel(self.timer.customer_name)
        self.customer_label.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_LARGE))
        self.customer_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        self.customer_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Area 1-2: Template name (smaller, regular, secondary)
        self.template_label = QLabel(self.template.name)
        self.template_label.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_MEDIUM))
        self.template_label.setStyleSheet(f"color: {Theme.Colors.TEXT_SECONDARY};")
        self.template_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Add with stretch for vertical centering (customer name first)
        layout.addStretch()
        layout.addWidget(self.customer_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.template_label, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addStretch()

        return container

    def _create_controls_area(self) -> QWidget:
        """Create Area 2: Play/Pause/Stop buttons with vertical centering."""
        container = QWidget()
        # Container takes full item height (no vertical margins)
        container.setFixedHeight(self._item_height)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(0)
        controls_layout.addStretch()

        self.start_btn = self._create_control_button("▶", "#43a047", "#2e7d32", "#1b5e20")
        self.pause_btn = self._create_control_button("⏸", "#fb8c00", "#f57c00", "#e65100")
        self.stop_btn = self._create_control_button("⏹", "#e53935", "#c62828", "#b71c1c")

        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.pause_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addStretch()

        # Add with stretch for vertical centering
        layout.addStretch()
        layout.addLayout(controls_layout)
        layout.addStretch()
        return container

    def _create_control_button(self, symbol: str, color: str, hover: str, pressed: str) -> QPushButton:
        """Create a control button with fixed 50px size."""
        btn = QPushButton(symbol)
        button_size = 50
        font_size = int(button_size * 0.60)  # 30px

        btn.setMinimumSize(button_size, button_size)
        btn.setMaximumSize(button_size, button_size)
        btn.setFlat(True)  # Remove default button styling on Windows
        btn.setStyleSheet(f"""
            QPushButton {{
                background: none;
                background-color: {Theme.Colors.PANEL_BACKGROUND};
                color: {color};
                border: none;
                font-size: {font_size}px;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: {Theme.Colors.PANEL_BACKGROUND};
                color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {Theme.Colors.PANEL_BACKGROUND};
                color: {pressed};
            }}
            QPushButton:disabled {{
                background-color: {Theme.Colors.PANEL_BACKGROUND};
                color: #bdbdbd;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        return btn

    def _create_time_area(self) -> QWidget:
        """Create Area 3: Time display."""
        self.time_label = QLabel("00 : 00")
        self.time_label.setFont(Theme.Fonts.timer_display())
        self.time_label.setStyleSheet(f"""
            color: {Theme.Colors.TEXT_PRIMARY};
            padding: 0px;
            margin: 0px;
        """)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return self._create_label_area(self.time_label)

    def _create_actions_area(self) -> QWidget:
        """Create Area 4: Edit/Delete buttons."""
        self.edit_btn = self._create_action_button("수정")
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.timer))

        self.delete_btn = self._create_action_button("삭제")
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.timer))

        return self._create_action_buttons_area(self.edit_btn, self.delete_btn)

    def update_display(self, minutes: int, seconds: int):
        """Update time display."""
        self.time_label.setText(format_time_display(minutes, seconds))

    def update_button_states(self, status: TimerStatus):
        """Update button enabled states based on timer status."""
        if status == TimerStatus.STOPPED:
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        elif status == TimerStatus.RUNNING:
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
        elif status == TimerStatus.PAUSED:
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)

    def update_customer_name(self, name: str):
        """Update customer name display."""
        self.timer.customer_name = name
        self.customer_label.setText(name)

    def update_template_name(self, name: str):
        """Update template name display."""
        self.template.name = name
        self.template_label.setText(name)

    def set_blink_border(self, show_border: bool):
        """Set blinking border state by changing border color only."""
        print(f"[DEBUG] set_blink_border called: show_border = {show_border}")

        if show_border:
            # Show blinking border - change color to green
            self.setStyleSheet(f"""
                TimerListItem {{
                    background-color: {Theme.Colors.COMPLETION_BACKGROUND};
                    border: 2px solid {Theme.Colors.COMPLETION_BORDER};
                    border-radius: {Theme.Spacing.RADIUS_LARGE}px;
                }}
            """)
        else:
            # Normal state - default gray border
            self.setStyleSheet(f"""
                TimerListItem {{
                    background-color: {Theme.Colors.PANEL_BACKGROUND};
                    border: 2px solid {Theme.Colors.BORDER};
                    border-radius: {Theme.Spacing.RADIUS_LARGE}px;
                }}
            """)

        print(f"[DEBUG] Border updated for show_border={show_border}")

    def mousePressEvent(self, event):
        """Handle mouse press event."""
        self.clicked.emit()
        super().mousePressEvent(event)
