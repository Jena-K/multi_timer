"""
Main application window.

Version: 1.0.2
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
import logging
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QSplitter, QMessageBox
)
from PySide6.QtCore import Qt
from services.database import DatabaseService
from models.base import get_current_time
from models.template import TimerTemplate
from models.timer import TimerInstance
from models.enums import TimerStatus
from ui.panels.template_panel import TemplatePanel
from ui.panels.timer_panel import TimerPanel
from ui.dialogs.template_dialog import TemplateDialog
from ui.dialogs.delete_template_dialog import DeleteTemplateDialog
from ui.dialogs.create_timer_dialog import CreateTimerDialog
from ui.dialogs.edit_timer_dialog import EditTimerDialog
from ui.theme import Theme

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window for Timer For Ryu."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.setWindowTitle("타이머 관리")
        self.setGeometry(100, 100, 1000, 600)

        # Initialize database service
        self.db = DatabaseService()

        # Initialize UI
        self._init_ui()

        # Load data from database
        self._load_templates()
        self._load_timers()

    def _init_ui(self):
        """Initialize UI components."""
        # Central widget with splitter for two-panel layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Template Management (30%)
        self.template_panel = TemplatePanel()
        self.template_panel.setMinimumWidth(250)
        self.template_panel.add_template_clicked.connect(self._on_add_template)
        self.template_panel.template_selected.connect(self._on_template_selected)
        self.template_panel.edit_template_clicked.connect(self._on_edit_template)
        self.template_panel.delete_template_clicked.connect(self._on_delete_template)
        self.template_panel.templates_reordered.connect(self._on_templates_reordered)
        splitter.addWidget(self.template_panel)

        # Right panel: Timer Panel
        self.timer_panel = TimerPanel()
        self.timer_panel.edit_timer_clicked.connect(self._on_edit_timer)
        self.timer_panel.delete_timer_clicked.connect(self._on_delete_timer)
        self.timer_panel.timer_completed.connect(self._on_timer_completed)
        self.timer_panel.timers_reordered.connect(self._on_timers_reordered)
        self.timer_panel.template_button_update_needed.connect(self._on_template_button_update)
        splitter.addWidget(self.timer_panel)

        # Set initial splitter sizes (30% / 70%)
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply global stylesheet
        self.setStyleSheet(Theme.Styles.main_window())

    def _load_templates(self):
        """Load templates from database."""
        templates = self.db.get_all_templates()
        self.template_panel.set_templates(templates)

    def _load_timers(self):
        """Load timers from database."""
        timers_with_templates = self.db.get_all_timers()
        self.timer_panel.set_timers(timers_with_templates)

        # Update template button states based on loaded timers
        self._update_all_template_buttons()

    def _on_add_template(self):
        """Handle add template button click."""
        dialog = TemplateDialog(parent=self)
        if dialog.exec():
            name, duration = dialog.get_template_data()

            # Get current max display_order
            templates = self.db.get_all_templates()
            max_order = max([t.display_order for t in templates], default=-1)

            # Create new template (will be at top with order 0)
            template = TimerTemplate.create(
                name=name,
                duration=duration,
                display_order=0
            )

            # Increment all existing template orders
            for existing_template in templates:
                existing_template.display_order += 1
                self.db.update_template(existing_template)

            # Save new template
            self.db.create_template(template)

            # Reload UI
            self._load_templates()

    def _on_template_selected(self, template: TimerTemplate):
        """
        Handle template card click (create timer from template).

        Args:
            template: Selected template
        """
        dialog = CreateTimerDialog(template=template, parent=self)
        if dialog.exec():
            customer_name = dialog.get_customer_name()

            # Get current max display_order for timers
            all_timers = self.db.get_all_timers()
            max_order = max([t[0].display_order for t in all_timers], default=-1)

            # Create new timer instance (will be at bottom with max_order + 1)
            timer = TimerInstance.create(
                customer_name=customer_name,
                template_id=template.id,
                initial_duration=template.duration,
                display_order=max_order + 1
            )

            # Save new timer (no need to update existing timers)
            self.db.create_timer(timer)

            # Reload UI
            self._load_timers()

    def _on_edit_template(self, template: TimerTemplate):
        """
        Handle edit template button click.

        Args:
            template: Template to edit
        """
        dialog = TemplateDialog(template=template, parent=self)
        if dialog.exec():
            name, duration = dialog.get_template_data()

            # Update template
            template.name = name
            template.duration = duration
            template.updated_at = get_current_time()

            # Save to database
            self.db.update_template(template)

            # Update template panel UI
            self.template_panel.update_template_item(template)

            # Update all child timers with new template data
            self.timer_panel.update_timers_by_template(template)

    def _on_delete_template(self, template: TimerTemplate):
        """
        Handle delete template button click.

        Args:
            template: Template to delete
        """
        # Get associated timers
        associated_timers = self.db.get_timers_by_template(str(template.id))

        # Show confirmation dialog
        dialog = DeleteTemplateDialog(
            template=template,
            associated_timers=associated_timers,
            parent=self
        )

        if dialog.exec():
            # Delete template (cascade deletes timers)
            self.db.delete_template(str(template.id))

            # Reload UI
            self._load_templates()
            self._load_timers()  # Also reload timers since they may be deleted

    def _on_edit_timer(self, timer: TimerInstance):
        """
        Handle edit timer button click.

        Args:
            timer: Timer to edit
        """
        dialog = EditTimerDialog(timer=timer, parent=self)
        if dialog.exec():
            customer_name = dialog.get_customer_name()

            # Update timer (only customer name)
            timer.customer_name = customer_name

            # Save to database
            self.db.update_timer(timer)

            # Update UI widget
            self.timer_panel.update_timer_item(timer)

    def _on_delete_timer(self, timer: TimerInstance):
        """
        Handle delete timer button click.

        Args:
            timer: Timer to delete
        """
        # Create custom styled message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("타이머 삭제")
        msg_box.setText(f'"{timer.customer_name}" 타이머를 삭제하시겠습니까?')
        msg_box.setInformativeText("이 작업은 되돌릴 수 없습니다.")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        # Apply Korean button text
        yes_btn = msg_box.button(QMessageBox.StandardButton.Yes)
        no_btn = msg_box.button(QMessageBox.StandardButton.No)
        yes_btn.setText("삭제")
        no_btn.setText("취소")

        # Apply theme styling
        msg_box.setStyleSheet(Theme.Styles.message_box("삭제", "취소"))

        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            # Delete from database
            self.db.delete_timer(str(timer.id))

            # Reload UI
            self._load_timers()

    def _on_timer_completed(self, timer: TimerInstance):
        """
        Handle timer completion.

        Args:
            timer: Completed timer instance
        """
        logger.info(f"Timer completed: {timer.customer_name}")

    def _on_templates_reordered(self, templates: list):
        """
        Handle template drag & drop reordering.

        Args:
            templates: Reordered list of templates
        """
        # Update display_order in database
        for i, template in enumerate(templates):
            template.display_order = i
            self.db.update_template(template)

    def _on_timers_reordered(self, timers: list):
        """
        Handle timer drag & drop reordering.

        Args:
            timers: Reordered list of timers
        """
        # Update display_order in database
        for i, timer in enumerate(timers):
            timer.display_order = i
            self.db.update_timer(timer)

    def _on_template_button_update(self, template_id: str, has_running_timers: bool):
        """
        Handle template button update request.

        Args:
            template_id: Template ID
            has_running_timers: Whether any child timers are running/paused
        """
        self.template_panel.update_template_buttons(template_id, has_running_timers)

    def _update_all_template_buttons(self):
        """Update all template buttons based on their child timer states."""
        # Get all templates
        templates = self.db.get_all_templates()

        for template in templates:
            # Check if any timer using this template is running or paused
            has_running_timers = False
            for item_widget in self.timer_panel.timer_items:
                if item_widget.timer.template_id == template.id:
                    if item_widget.timer.status in [TimerStatus.RUNNING, TimerStatus.PAUSED]:
                        has_running_timers = True
                        break

            # Update template buttons
            self.template_panel.update_template_buttons(str(template.id), has_running_timers)
