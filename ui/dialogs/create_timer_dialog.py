"""
Create timer from template dialog.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt
from models.template import TimerTemplate
from ui.theme import Theme


class CreateTimerDialog(QDialog):
    """Dialog for creating a timer from a template."""

    def __init__(self, template: TimerTemplate, parent=None):
        """
        Initialize create timer dialog.

        Args:
            template: Template to create timer from
            parent: Parent widget
        """
        super().__init__(parent)
        self.template = template
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("타이머 생성")
        self.setModal(True)
        self.setFixedSize(450, 200)
        self.setStyleSheet(Theme.Styles.dialog())

        layout = QVBoxLayout()
        layout.setSpacing(Theme.Spacing.PADDING_XLARGE + 4)  # 20px
        layout.setContentsMargins(30, 30, 30, 30)

        # Grid layout for form
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)

        # Template Name Row (read-only)
        template_label = QLabel("템플릿")
        template_label.setFont(Theme.Fonts.label())
        template_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(template_label, 0, 0, Qt.AlignmentFlag.AlignRight)

        template_value = QLabel(self.template.name)
        template_value.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM))
        template_value.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(template_value, 0, 1)

        # Duration Row (read-only)
        total_seconds = int(self.template.duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        duration_label = QLabel("타이머 시간")
        duration_label.setFont(Theme.Fonts.label())
        duration_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(duration_label, 1, 0, Qt.AlignmentFlag.AlignRight)

        duration_value = QLabel(f"{minutes:02d} : {seconds:02d}")
        duration_value.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_MEDIUM))
        duration_value.setStyleSheet(f"color: {Theme.Colors.TEXT_SECONDARY};")
        form_layout.addWidget(duration_value, 1, 1)

        # Customer Name Row
        name_label = QLabel("고객명")
        name_label.setFont(Theme.Fonts.label())
        name_label.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")
        form_layout.addWidget(name_label, 2, 0, Qt.AlignmentFlag.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("고객명 입력")
        self.name_input.setFont(Theme.Fonts.input())
        self.name_input.setStyleSheet(Theme.Styles.input_field())
        self.name_input.returnPressed.connect(self._on_create)  # Enter key triggers create
        self.name_input.setFocus()
        form_layout.addWidget(self.name_input, 2, 1)

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

        create_btn = QPushButton("생성")
        create_btn.setFixedSize(100, 35)
        create_btn.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM))
        create_btn.setStyleSheet(f"""
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
        create_btn.clicked.connect(self._on_create)
        button_layout.addWidget(create_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _on_create(self):
        """Validate and create timer."""
        customer_name = self.name_input.text().strip()

        if not customer_name:
            QMessageBox.warning(self, "입력 오류", "고객명을 입력해주세요.")
            return

        # Store validated data
        self.validated_customer_name = customer_name
        self.accept()

    def get_customer_name(self) -> str:
        """
        Get validated customer name.

        Returns:
            str: Customer name
        """
        return self.validated_customer_name
