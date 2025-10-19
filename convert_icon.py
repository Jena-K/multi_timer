"""
Convert PNG to ICO for Windows executable icon.

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-20
Last Modified: 2025-10-20

Usage:
    uv pip install pillow
    uv run python convert_icon.py
"""
from PIL import Image
from pathlib import Path


def convert_png_to_ico():
    """Convert dasan.png to dasan.ico for Windows."""
    assets_dir = Path(__file__).parent / "assets"
    png_path = assets_dir / "dasan.png"
    ico_path = assets_dir / "dasan.ico"

    if not png_path.exists():
        print(f"Error: {png_path} not found!")
        return False

    print(f"Converting {png_path} to {ico_path}...")

    try:
        # Open PNG image
        img = Image.open(png_path)

        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Create ICO with multiple sizes (256, 128, 64, 32, 16)
        icon_sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]

        # Save as ICO
        img.save(ico_path, format='ICO', sizes=icon_sizes)

        print(f"✅ Icon created successfully: {ico_path}")
        return True

    except Exception as e:
        print(f"❌ Error converting icon: {e}")
        return False


if __name__ == "__main__":
    import sys
    success = convert_png_to_ico()
    sys.exit(0 if success else 1)
