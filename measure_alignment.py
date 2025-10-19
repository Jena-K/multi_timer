"""
Measure actual widget positions to detect vertical asymmetry.
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from datetime import timedelta
from models.template import TimerTemplate
from ui.widgets.template_list_item import TemplateListItem


def measure_vertical_centering(item):
    """Measure vertical centering of widgets."""
    print("\n" + "="*80)
    print("VERTICAL CENTERING ANALYSIS")
    print("="*80 + "\n")

    item_height = item.height()
    item_center = item_height / 2

    print(f"Item height: {item_height}px")
    print(f"Theoretical center: {item_center}px\n")

    # Measure main layout
    layout_margins = item.layout().contentsMargins()
    print(f"Main Layout Margins: Top={layout_margins.top()}px, Bottom={layout_margins.bottom()}px")

    # Calculate content area
    content_top = layout_margins.top()
    content_bottom = item_height - layout_margins.bottom()
    content_height = content_bottom - content_top
    content_center = content_top + (content_height / 2)

    print(f"Content area: {content_top}px to {content_bottom}px (height: {content_height}px)")
    print(f"Content center: {content_center}px")
    print(f"Offset from item center: {content_center - item_center}px\n")

    # Measure name label position
    name_container = item.layout().itemAt(0).widget()
    name_label = item.name_label

    name_label_height = name_label.height()
    # Get label position within container
    label_y_in_container = name_label.y()

    # Since container is centered, calculate label's actual position
    container_height = name_container.height()

    print(f"Name Label:")
    print(f"  Label height: {name_label_height}px")
    print(f"  Container height: {container_height}px")
    print(f"  Label Y position in container: {label_y_in_container}px")

    # Calculate visual position
    # The container is at content_top, and label is centered within container
    label_top = content_top + label_y_in_container
    label_bottom = label_top + name_label_height
    label_center = label_top + (name_label_height / 2)

    print(f"  Visual position: {label_top}px to {label_bottom}px")
    print(f"  Visual center: {label_center}px")
    print(f"  Offset from item center: {label_center - item_center}px")

    # Calculate padding distances
    top_padding = label_top
    bottom_padding = item_height - label_bottom

    print(f"\n  Top padding (item top to label top): {top_padding}px")
    print(f"  Bottom padding (label bottom to item bottom): {bottom_padding}px")
    print(f"  Asymmetry: {abs(top_padding - bottom_padding)}px")

    if abs(top_padding - bottom_padding) > 1:
        print(f"\n⚠️  VISUAL ASYMMETRY DETECTED!")
        if top_padding > bottom_padding:
            print(f"  Top padding is {top_padding - bottom_padding}px LARGER than bottom padding")
        else:
            print(f"  Bottom padding is {bottom_padding - top_padding}px LARGER than top padding")

    # Measure button area
    print(f"\nButton Area:")
    button_container = item.layout().itemAt(2).widget()
    button_height = button_container.height()
    print(f"  Button area height: {button_height}px")
    print(f"  Buttons are vertically centered within their {button_height}px area")

    total_button_height = item.edit_btn.height() + item.delete_btn.height()
    button_padding = button_height - total_button_height
    print(f"  Total button height: {total_button_height}px")
    print(f"  Padding around buttons: {button_padding}px")


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
    item.setMinimumWidth(500)

    # Create window
    window = QMainWindow()
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(item)
    layout.addStretch()
    window.setCentralWidget(container)
    window.setGeometry(100, 100, 600, 200)
    window.show()

    # Wait for layout
    app.processEvents()

    measure_vertical_centering(item)

    print("\n" + "="*80)

    sys.exit(0)


if __name__ == "__main__":
    main()
