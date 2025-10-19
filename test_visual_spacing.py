"""
Visual test to see actual rendering and measure visual padding.
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor
from datetime import timedelta
from models.template import TimerTemplate
from ui.widgets.template_list_item import TemplateListItem


class DebugWidget(QWidget):
    """Widget with visual debug lines."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(500)

    def paintEvent(self, event):
        """Draw debug lines."""
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0, 128), 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        # Find template item
        for child in self.findChildren(TemplateListItem):
            item_y = child.y()
            item_height = child.height()

            # Draw top edge
            painter.drawLine(0, item_y, self.width(), item_y)

            # Draw bottom edge
            painter.drawLine(0, item_y + item_height, self.width(), item_y + item_height)

            # Draw center line
            center_y = item_y + item_height // 2
            painter.setPen(QPen(QColor(0, 255, 0, 128), 2, Qt.PenStyle.SolidLine))
            painter.drawLine(0, center_y, self.width(), center_y)

            # Find QLabel positions
            painter.setPen(QPen(QColor(0, 0, 255, 128), 1, Qt.PenStyle.DotLine))
            for label in child.findChildren(QLabel):
                label_global_pos = label.mapTo(self, label.rect().topLeft())
                label_y = label_global_pos.y()
                label_height = label.height()

                # Draw label top
                painter.drawLine(0, label_y, self.width(), label_y)
                # Draw label bottom
                painter.drawLine(0, label_y + label_height, self.width(), label_y + label_height)

                # Measure distances
                top_distance = label_y - item_y
                bottom_distance = (item_y + item_height) - (label_y + label_height)

                print(f"\nLabel: {label.text()[:20]}...")
                print(f"  Item top to label top: {top_distance}px")
                print(f"  Label bottom to item bottom: {bottom_distance}px")
                print(f"  Difference: {abs(top_distance - bottom_distance)}px")

            break


def main():
    """Main test function."""
    app = QApplication(sys.argv)

    # Create test template
    template = TimerTemplate.create(
        name="Test Template with Long Name",
        duration=timedelta(minutes=5, seconds=30),
        display_order=0
    )

    # Create window
    window = QMainWindow()
    container = DebugWidget()
    layout = QVBoxLayout(container)

    # Add instruction label
    instruction = QLabel("Visual Debug Test\nRed dashed = item boundaries\nGreen solid = item center\nBlue dotted = label boundaries")
    instruction.setStyleSheet("background: white; padding: 10px; border: 1px solid black;")
    layout.addWidget(instruction)

    # Create template list item
    item = TemplateListItem(template)
    layout.addWidget(item)

    layout.addStretch()

    window.setCentralWidget(container)
    window.setGeometry(100, 100, 600, 300)
    window.show()

    # Force repaint
    app.processEvents()
    container.update()

    print("\n" + "="*80)
    print("VISUAL SPACING ANALYSIS")
    print("="*80)

    # Don't exit - show window for visual inspection
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
