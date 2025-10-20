"""
Edit timer dialog.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout

from models.timer import TimerInstance
from ui.theme import Theme


class EditTimerDialog(QDialog):
    """Dialog for editing timer (only when STOPPED)."""

    def __init__(self, timer: TimerInstance, parent=None):
        """
        Initialize edit timer dialog.

        Args:
            timer: Timer instance to edit
            parent: Parent widget
        """
        super().__init__(parent)
        self.timer = timer
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("타이머 수정")
        self.setModal(True)
        self.setFixedSize(450, 150)
        self.setStyleSheet(Theme.Styles.dialog())

        layout = QVBoxLayout()
        layout.setSpacing(Theme.Spacing.PADDING_XLARGE + 4)  # 20px
        layout.setContentsMargins(30, 30, 30, 30)

        # Grid layout for form
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        # Customer Name Row
        name_label = QLabel("고객명")
        name_label.setFont(Theme.Fonts.label())
        name_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(name_label, 0, 0, Qt.AlignmentFlag.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setText(self.timer.customer_name)
        self.name_input.setPlaceholderText("고객명 입력")
        self.name_input.setFont(Theme.Fonts.input())
        self.name_input.setStyleSheet(Theme.Styles.input_field())
        self.name_input.returnPressed.connect(self._on_save)  # Enter key triggers save
        self.name_input.setFocus()
        form_layout.addWidget(self.name_input, 0, 1)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("취소")
        cancel_btn.setFixedSize(100, 35)
        cancel_btn.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_MEDIUM))
        cancel_btn.setStyleSheet(f"""
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
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("저장")
        save_btn.setFixedSize(100, 35)
        save_btn.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM))
        save_btn.setStyleSheet(f"""
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
        save_btn.clicked.connect(self._on_save)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_save(self):
        """Validate and save changes."""
        # Validate name only
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "입력 오류", "고객명을 입력해주세요.")
            return

        # Store validated data
        self.validated_name = name

        self.accept()

    def get_customer_name(self) -> str:
        """
        Get validated customer name.

        Returns:
            str: Customer name
        """
        return self.validated_name
