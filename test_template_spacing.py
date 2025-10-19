"""
Test script to measure template list item spacing.

This script creates a template list item and measures all spacing values
to identify the source of uneven vertical padding.
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from datetime import timedelta
from models.template import TimerTemplate
from ui.widgets.template_list_item import TemplateListItem


def analyze_widget_spacing(widget, name, level=0):
    """Recursively analyze widget spacing."""
    indent = "  " * level
    print(f"{indent}{name} ({widget.__class__.__name__}):")

    # Widget size
    print(f"{indent}  Size: {widget.width()} x {widget.height()}")

    # Widget margins
    margins = widget.contentsMargins()
    print(f"{indent}  Margins (L,T,R,B): {margins.left()}, {margins.top()}, {margins.right()}, {margins.bottom()}")

    # Layout if exists
    if widget.layout():
        layout = widget.layout()
        print(f"{indent}  Layout: {layout.__class__.__name__}")
        layout_margins = layout.contentsMargins()
        print(f"{indent}  Layout Margins (L,T,R,B): {layout_margins.left()}, {layout_margins.top()}, {layout_margins.right()}, {layout_margins.bottom()}")
        print(f"{indent}  Layout Spacing: {layout.spacing()}")

        # Analyze layout items
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget():
                analyze_widget_spacing(item.widget(), f"Item {i}", level + 1)


def main():
    """Main test function."""
    app = QApplication(sys.argv)

    # Create test template
    template = TimerTemplate.create(
        name="Test Template",
        duration=timedelta(minutes=5, seconds=30),
        display_order=0
    )

    # Create template list item
    item = TemplateListItem(template)
    item.setMinimumWidth(400)

    # Create window to display
    window = QMainWindow()
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(item)
    layout.addStretch()
    window.setCentralWidget(container)
    window.setGeometry(100, 100, 500, 200)
    window.show()

    # Wait for widget to be rendered
    app.processEvents()

    print("\n" + "="*80)
    print("TEMPLATE LIST ITEM SPACING ANALYSIS")
    print("="*80 + "\n")

    print(f"Item fixed height: {item._item_height}px")
    print(f"Actual height: {item.height()}px\n")

    # Analyze main item
    analyze_widget_spacing(item, "TemplateListItem (Root)")

    print("\n" + "="*80)
    print("SPECIFIC MEASUREMENTS")
    print("="*80 + "\n")

    # Check QLabel specific properties
    print("QLabel Analysis:")
    print(f"  Name Label font: {item.name_label.font().family()}, {item.name_label.font().pointSize()}pt")
    print(f"  Name Label size: {item.name_label.width()} x {item.name_label.height()}")
    print(f"  Name Label sizeHint: {item.name_label.sizeHint()}")
    print(f"  Name Label minimumSizeHint: {item.name_label.minimumSizeHint()}")

    # Font metrics
    from PySide6.QtGui import QFontMetrics
    fm = QFontMetrics(item.name_label.font())
    print(f"  Font metrics - height: {fm.height()}, ascent: {fm.ascent()}, descent: {fm.descent()}, leading: {fm.leading()}")

    print("\n" + "="*80)
    print("VERTICAL SPACE CALCULATION")
    print("="*80 + "\n")

    # Calculate vertical space usage
    layout_margins = item.layout().contentsMargins()
    top_margin = layout_margins.top()
    bottom_margin = layout_margins.bottom()

    print(f"Item height: {item._item_height}px")
    print(f"Top margin: {top_margin}px")
    print(f"Bottom margin: {bottom_margin}px")
    print(f"Available content height: {item._item_height - top_margin - bottom_margin}px")
    print(f"Font height: {fm.height()}px")
    print(f"Unused vertical space: {item._item_height - top_margin - bottom_margin - fm.height()}px")

    # Check if there's asymmetry
    if top_margin != bottom_margin:
        print(f"\n⚠️  ASYMMETRY DETECTED: Top margin ({top_margin}px) != Bottom margin ({bottom_margin}px)")
        print(f"   Difference: {abs(top_margin - bottom_margin)}px")

    print("\n" + "="*80)

    # Exit without showing window
    sys.exit(0)


if __name__ == "__main__":
    main()
