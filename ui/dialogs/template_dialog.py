"""
Add/Edit template dialog.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt
from datetime import timedelta
from typing import Optional
from models.template import TimerTemplate
from ui.theme import Theme


class TemplateDialog(QDialog):
    """Dialog for adding or editing templates."""

    def __init__(self, template: Optional[TimerTemplate] = None, parent=None):
        """
        Initialize template dialog.

        Args:
            template: Existing template to edit (None for new template)
            parent: Parent widget
        """
        super().__init__(parent)
        self.template = template
        self.is_edit_mode = template is not None
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("템플릿 수정" if self.is_edit_mode else "새 템플릿 추가")
        self.setModal(True)
        self.setFixedSize(450, 180)
        self.setStyleSheet(Theme.Styles.dialog())

        layout = QVBoxLayout()
        layout.setSpacing(Theme.Spacing.PADDING_XLARGE + 4)  # 20px
        layout.setContentsMargins(30, 30, 30, 30)

        # Grid layout for form
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        # Template Name Row
        name_label = QLabel("템플릿 이름")
        name_label.setFont(Theme.Fonts.label())
        name_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(name_label, 0, 0, Qt.AlignmentFlag.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("템플릿 이름 입력")
        self.name_input.setFont(Theme.Fonts.input())
        self.name_input.setStyleSheet(Theme.Styles.input_field())
        self.name_input.returnPressed.connect(self._on_save)  # Enter key triggers save
        if self.template:
            self.name_input.setText(self.template.name)
        form_layout.addWidget(self.name_input, 0, 1)

        # Duration Row
        duration_label = QLabel("타이머 시간")
        duration_label.setFont(Theme.Fonts.label())
        duration_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(duration_label, 1, 0, Qt.AlignmentFlag.AlignRight)

        # Duration input layout
        duration_layout = QHBoxLayout()
        duration_layout.setSpacing(Theme.Spacing.MARGIN_MEDIUM)

        self.minutes_input = QLineEdit()
        self.minutes_input.setPlaceholderText("MM")
        self.minutes_input.setMaxLength(2)
        self.minutes_input.setFixedWidth(Theme.Spacing.INPUT_WIDTH_SMALL)
        self.minutes_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.minutes_input.setFont(Theme.Fonts.input())
        self.minutes_input.setStyleSheet(Theme.Styles.input_field())
        self.minutes_input.returnPressed.connect(self._on_save)  # Enter key triggers save

        colon_label = QLabel(":")
        colon_label.setFont(Theme.Fonts.bold(16))
        colon_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")

        self.seconds_input = QLineEdit()
        self.seconds_input.setPlaceholderText("SS")
        self.seconds_input.setMaxLength(2)
        self.seconds_input.setFixedWidth(Theme.Spacing.INPUT_WIDTH_SMALL)
        self.seconds_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.seconds_input.setFont(Theme.Fonts.input())
        self.seconds_input.setStyleSheet(Theme.Styles.input_field())
        self.seconds_input.returnPressed.connect(self._on_save)  # Enter key triggers save

        if self.template:
            total_seconds = int(self.template.duration.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            self.minutes_input.setText(f"{minutes:02d}")
            self.seconds_input.setText(f"{seconds:02d}")
        else:
            # Default: 5 minutes 00 seconds
            self.minutes_input.setText("05")
            self.seconds_input.setText("00")

        duration_layout.addWidget(self.minutes_input)
        duration_layout.addWidget(colon_label)
        duration_layout.addWidget(self.seconds_input)
        duration_layout.addStretch()

        form_layout.addLayout(duration_layout, 1, 1)

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
        """Validate and save template."""
        # Validate name
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "입력 오류", "템플릿 이름을 입력해주세요.")
            return

        # Validate duration
        try:
            minutes_text = self.minutes_input.text().strip()
            seconds_text = self.seconds_input.text().strip()

            if not minutes_text or not seconds_text:
                raise ValueError("시간을 입력해주세요")

            minutes = int(minutes_text)
            seconds = int(seconds_text)

            if minutes < 0 or minutes > 99:
                raise ValueError("분은 00에서 99 사이여야 합니다")

            if seconds < 0 or seconds > 59:
                raise ValueError("초는 00에서 59 사이여야 합니다")

            if minutes == 0 and seconds == 0:
                raise ValueError("시간은 0보다 커야 합니다")

            duration = timedelta(minutes=minutes, seconds=seconds)

        except ValueError as e:
            QMessageBox.warning(self, "입력 오류", str(e))
            return

        # Store validated data
        self.validated_name = name
        self.validated_duration = duration

        self.accept()

    def get_template_data(self) -> tuple[str, timedelta]:
        """
        Get validated template data.

        Returns:
            tuple: (name, duration)
        """
        return self.validated_name, self.validated_duration
