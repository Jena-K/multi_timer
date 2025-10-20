"""
Toast message utility for user notifications.

Version: 1.0.1
Author: rowan@lionrocket.ai
Created: 2025-10-19
Last Modified: 2025-10-19
"""
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect, QLabel

from ui.theme import Theme


class ToastMessage(QLabel):
    """Toast notification widget."""

    # Animation constants
    ANIMATION_DURATION = 200  # milliseconds
    DEFAULT_DISPLAY_DURATION = 2000  # milliseconds
    BOTTOM_MARGIN = 50  # pixels from bottom
    MAX_WIDTH = 400  # maximum toast width

    def __init__(self, message: str, parent=None):
        """
        Initialize toast message.

        Args:
            message: Message text to display
            parent: Parent widget
        """
        super().__init__(message, parent)
        self._animation = None  # Keep reference to prevent garbage collection
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setFont(Theme.Fonts.regular(Theme.Fonts.SIZE_MEDIUM))
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.Colors.TOAST_BACKGROUND};
                color: {Theme.Colors.TOAST_TEXT};
                padding: {Theme.Spacing.PADDING_LARGE}px {Theme.Spacing.PADDING_XLARGE + 4}px;
                border-radius: {Theme.Spacing.RADIUS_MEDIUM}px;
            }}
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setMaximumWidth(self.MAX_WIDTH)

        # Create opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)

    def show_toast(self, duration: int = None):
        """
        Show toast message with fade animation.

        Args:
            duration: Display duration in milliseconds (default: DEFAULT_DISPLAY_DURATION)
        """
        if duration is None:
            duration = self.DEFAULT_DISPLAY_DURATION

        # Position at center bottom
        self._position_toast()

        # Show with fade in
        self.show()
        self.raise_()

        # Fade in animation
        self._animation = self._create_fade_animation(
            start_opacity=0.0,
            end_opacity=1.0
        )
        self._animation.start()

        # Auto hide after duration
        QTimer.singleShot(duration, self._fade_out)

    def _position_toast(self):
        """Position toast at center bottom of parent."""
        if self.parent():
            parent_rect = self.parent().rect()
            self.adjustSize()
            x = (parent_rect.width() - self.width()) // 2
            y = parent_rect.height() - self.height() - self.BOTTOM_MARGIN
            self.move(x, y)

    def _create_fade_animation(self, start_opacity: float, end_opacity: float) -> QPropertyAnimation:
        """
        Create fade animation with consistent settings.

        Args:
            start_opacity: Starting opacity value (0.0 - 1.0)
            end_opacity: Ending opacity value (0.0 - 1.0)

        Returns:
            QPropertyAnimation: Configured animation object
        """
        animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        animation.setDuration(self.ANIMATION_DURATION)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation

    def _fade_out(self):
        """Fade out and hide toast."""
        self._animation = self._create_fade_animation(
            start_opacity=1.0,
            end_opacity=0.0
        )
        self._animation.finished.connect(self.hide)
        self._animation.start()


def show_toast(parent, message: str, duration: int = None):
    """
    Show a toast message.

    Args:
        parent: Parent widget
        message: Message text to display
        duration: Display duration in milliseconds (default: ToastMessage.DEFAULT_DISPLAY_DURATION)

    Returns:
        ToastMessage: Toast instance (for testing or advanced usage)
    """
    toast = ToastMessage(message, parent)
    toast.show_toast(duration)
    return toast
