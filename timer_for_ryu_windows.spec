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
        # Exclude unnecessary PySide6 modules
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtSql',
        # QtNetwork removed from excludes - required by QSoundEffect/QMultimedia
        'PySide6.QtOpenGL',
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtBluetooth',
        'PySide6.QtDBus',
        'PySide6.QtDesigner',
        'PySide6.QtHelp',
        'PySide6.QtLocation',
        'PySide6.QtNfc',
        'PySide6.QtPositioning',
        'PySide6.QtPrintSupport',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtSensors',
        'PySide6.QtSerialPort',
        'PySide6.QtTest',
        'PySide6.QtTextToSpeech',
        'PySide6.QtWebChannel',
        'PySide6.QtWebSockets',
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
        'IPython',
        'jupyter',
        'notebook',
        # Exclude development tools
        'pytest',
        'unittest',
        'doctest',
        'pdb',
        'pydoc',
        # Exclude other heavy packages
        'tkinter',
        'PIL.ImageQt',
        'setuptools',
        'distutils',
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
    console=True,  # Windows에서 폰트 로딩 디버그를 위해 콘솔 표시 (배포 시 False로 변경)
    icon='assets/dasan.ico',
)
