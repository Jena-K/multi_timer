"""
Delete template confirmation dialog.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from models.template import TimerTemplate
from models.timer import TimerInstance
from ui.theme import Theme


class DeleteTemplateDialog(QDialog):
    """Confirmation dialog for template deletion with timer warning."""

    def __init__(
        self,
        template: TimerTemplate,
        associated_timers: List[TimerInstance],
        parent=None
    ):
        """
        Initialize delete confirmation dialog.

        Args:
            template: Template to delete
            associated_timers: List of timers using this template
            parent: Parent widget
        """
        super().__init__(parent)
        self.template = template
        self.associated_timers = associated_timers
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("템플릿 삭제")
        self.setModal(True)
        self.setFixedWidth(450)
        self.setStyleSheet(Theme.Styles.dialog())

        layout = QVBoxLayout()
        layout.setSpacing(Theme.Spacing.PADDING_XLARGE)
        layout.setContentsMargins(30, 30, 30, 30)

        # Warning icon and title (if has timers)
        if self.associated_timers:
            title = QLabel("⚠️ 템플릿 삭제 경고")
            title.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_LARGE + 1))
            title.setStyleSheet(f"color: {Theme.Colors.DANGER};")
        else:
            title = QLabel("템플릿 삭제")
            title.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_LARGE + 1))
            title.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY};")

        layout.addWidget(title)

        # Message
        if self.associated_timers:
            message = QLabel(
                f'"{self.template.name}" 템플릿을 삭제하면\n'
                f'다음 활성 타이머들도 함께 삭제됩니다:'
            )
        else:
            message = QLabel(
                f'"{self.template.name}" 템플릿을\n'
                f'삭제하시겠습니까?'
            )

        message.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_NORMAL))
        message.setStyleSheet(f"color: {Theme.Colors.TEXT_PRIMARY}; padding: 10px 0;")
        message.setWordWrap(True)
        layout.addWidget(message)

        # Timer list (if exists)
        if self.associated_timers:
            timer_list_widget = QWidget()
            timer_list_layout = QVBoxLayout()
            timer_list_layout.setSpacing(5)
            timer_list_layout.setContentsMargins(10, 10, 10, 10)

            for timer in self.associated_timers:
                # Format: • Customer Name (MM:SS)
                total_seconds = int(timer.remaining_time.total_seconds())
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                time_str = f"{minutes:02d}:{seconds:02d}"

                timer_label = QLabel(f"• {timer.customer_name} ({time_str})")
                timer_label.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_NORMAL - 1))
                timer_label.setStyleSheet(f"color: {Theme.Colors.TEXT_SECONDARY}; padding: 2px;")
                timer_list_layout.addWidget(timer_label)

            timer_list_widget.setLayout(timer_list_layout)
            timer_list_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {Theme.Colors.BACKGROUND};
                    border-radius: {Theme.Spacing.RADIUS_SMALL}px;
                }}
            """)
            layout.addWidget(timer_list_widget)

            # Total count
            total_label = QLabel(f"총 {len(self.associated_timers)}개의 타이머가 삭제됩니다")
            total_label.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_NORMAL - 1))
            total_label.setStyleSheet(f"color: {Theme.Colors.DANGER}; padding: 5px 0;")
            layout.addWidget(total_label)

        # Warning message
        warning = QLabel("이 작업은 되돌릴 수 없습니다.")
        warning.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_NORMAL - 2))
        warning.setStyleSheet(f"color: {Theme.Colors.TEXT_TERTIARY}; font-style: italic;")
        layout.addWidget(warning)

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

        delete_btn = QPushButton("모두 삭제" if self.associated_timers else "삭제")
        delete_btn.setFixedSize(100, 35)
        delete_btn.setFont(Theme.Fonts.bold(Theme.Fonts.SIZE_MEDIUM))
        delete_btn.setStyleSheet(f"""
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
        delete_btn.clicked.connect(self.accept)
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)
