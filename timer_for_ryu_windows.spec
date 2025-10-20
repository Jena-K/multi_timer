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
    console=True,  # Windows에서 폰트 로딩 디버그를 위해 콘솔 표시 (배포 시 False로 변경)
    icon='assets/dasan.ico',
)
