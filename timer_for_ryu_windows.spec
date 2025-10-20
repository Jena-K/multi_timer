# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/alert.wav', 'assets'),
        # Include entire fonts directory to ensure all font files are bundled
        ('assets/fonts', 'assets/fonts'),
        # Include SVG icons for control buttons
        ('assets/icons', 'assets/icons'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
        'PySide6.QtMultimedia',
        'PySide6.QtSvg',  # For SVG icon rendering
        # Ensure platform plugins are included
        'PySide6.QtPlatform',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Only exclude very large, clearly unused modules
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineWidgets',
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        # Exclude scientific packages
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        # Exclude development tools
        'pytest',
        'IPython',
        'jupyter',
    ],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Timer For Ryu',
    debug=False,
    strip=True,  # Strip symbols to reduce size
    upx=True,  # Enable UPX compression
    upx_exclude=[
        # Exclude problematic DLLs from UPX compression
        'Qt6Core.dll',
        'Qt6Gui.dll',
        'Qt6Widgets.dll',
        'Qt6Multimedia.dll',
        'Qt6Svg.dll',
    ],
    console=True,  # Keep console visible for debugging
    icon='assets/dasan.ico',
    bootloader_ignore_signals=False,  # Better error reporting
)
