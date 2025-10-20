# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/alert.wav', 'assets'),
        ('assets/fonts/Pretendard-Regular.otf', 'assets/fonts'),
        ('assets/fonts/Pretendard-Bold.otf', 'assets/fonts'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
        'PySide6.QtMultimedia',
        # Ensure platform plugins are included
        'PySide6.QtPlatform',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtSql',
        'PySide6.QtNetwork',
        'PySide6.QtOpenGL',
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineWidgets',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
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
    strip=False,
    upx=False,  # PySide6 DLL 손상 방지
    console=False,
    icon='assets/dasan.ico',
)
