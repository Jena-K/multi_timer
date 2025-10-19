"""
Base dialog class with common functionality.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtWidgets import QDialog, QPushButton, QHBoxLayout, QMessageBox, QGridLayout
from ui.theme import Theme


class BaseDialog(QDialog):
    """Base class for dialogs with common styling and button creation."""

    # Dialog size constants
    DIALOG_WIDTH = 450
    DIALOG_PADDING = 30
    FORM_SPACING_H = 15
    FORM_SPACING_V = 15

    # Button constants
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 35

    def __init__(self, title: str, parent=None):
        """
        Initialize base dialog.

        Args:
            title: Dialog window title
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setStyleSheet(Theme.Styles.dialog())

    def _create_form_layout(self) -> QGridLayout:
        """
        Create grid layout for form with standard spacing.

        Returns:
            QGridLayout: Configured form layout
        """
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(self.FORM_SPACING_H)
        form_layout.setVerticalSpacing(self.FORM_SPACING_V)
        return form_layout

    def _create_button_layout(self, cancel_text: str = "취소",
                              action_text: str = "저장",
                              is_danger: bool = False) -> QHBoxLayout:
        """
        Create button layout with cancel and action buttons.

        Args:
            cancel_text: Cancel button text
            action_text: Action button text (e.g., "저장", "생성", "삭제")
            is_danger: Whether action button should use danger styling

        Returns:
            QHBoxLayout: Layout with configured buttons
        """
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Cancel button
        cancel_btn = self._create_cancel_button(cancel_text)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        # Action button (save/create/delete)
        if is_danger:
            action_btn = self._create_danger_button(action_text)
        else:
            action_btn = self._create_primary_button(action_text)

        # Store button reference for subclass to connect
        self.action_button = action_btn
        button_layout.addWidget(action_btn)

        return button_layout

    def _create_cancel_button(self, text: str) -> QPushButton:
        """
        Create cancel button with standard styling.

        Args:
            text: Button text

        Returns:
            QPushButton: Configured cancel button
        """
        btn = QPushButton(text)
        btn.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        btn.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_MEDIUM))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #95a5a6;
                color: {Theme.Colors.WHITE};
                border: none;
                border-radius: {Theme.Spacing.RADIUS_SMALL}px;
            }}
            QPushButton:hover {{
                background-color: #7f8c8d;
            }}
        """)
        return btn

    def _create_primary_button(self, text: str) -> QPushButton:
        """
        Create primary action button.

        Args:
            text: Button text

        Returns:
            QPushButton: Configured primary button
        """
        btn = QPushButton(text)
        btn.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        btn.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.Colors.PRIMARY};
                color: {Theme.Colors.WHITE};
                border: none;
                border-radius: {Theme.Spacing.RADIUS_SMALL}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.Colors.PRIMARY_HOVER};
            }}
        """)
        return btn

    def _create_danger_button(self, text: str) -> QPushButton:
        """
        Create danger action button (for delete operations).

        Args:
            text: Button text

        Returns:
            QPushButton: Configured danger button
        """
        btn = QPushButton(text)
        btn.setFixedSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        btn.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.Colors.DANGER};
                color: {Theme.Colors.WHITE};
                border: none;
                border-radius: {Theme.Spacing.RADIUS_SMALL}px;
            }}
            QPushButton:hover {{
                background-color: {Theme.Colors.DANGER_HOVER};
            }}
        """)
        return btn

    def _show_warning(self, title: str, message: str):
        """
        Show warning message box.

        Args:
            title: Warning dialog title
            message: Warning message
        """
        QMessageBox.warning(self, title, message)
