"""
SVG icon loader utility for creating QIcon from SVG files with color support.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-20

Usage:
    from ui.utils.icon_loader import create_svg_icon

    icon = create_svg_icon("play.svg", "#43a047", size=30)
    button.setIcon(icon)
"""
import sys
from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize


def get_icon_path(icon_name: str) -> Path:
    """
    Get the full path to an SVG icon file.

    Args:
        icon_name: Name of the SVG file (e.g., "play.svg")

    Returns:
        Path: Full path to the icon file
    """
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent.parent

    return base_path / "assets" / "icons" / icon_name


def create_svg_icon(icon_name: str, color: str, size: int = 24) -> QIcon:
    """
    Create a QIcon from an SVG file with specified color.

    Args:
        icon_name: Name of the SVG file (e.g., "play.svg")
        color: Color in hex format (e.g., "#43a047")
        size: Icon size in pixels (default: 24)

    Returns:
        QIcon: Colored icon at specified size
    """
    icon_path = get_icon_path(icon_name)

    if not icon_path.exists():
        print(f"[ICON] Warning: Icon file not found: {icon_path}")
        return QIcon()

    # Read SVG file
    with open(icon_path, 'r', encoding='utf-8') as f:
        svg_data = f.read()

    # Replace currentColor with actual color
    svg_data = svg_data.replace('currentColor', color)

    # Create SVG renderer
    renderer = QSvgRenderer(svg_data.encode('utf-8'))

    # Create pixmap and render SVG
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(QColor(0, 0, 0, 0))  # Transparent background

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)
