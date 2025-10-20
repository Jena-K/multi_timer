# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

# Windows에서 PySide6 플러그인 경로 찾기
def get_pyside6_plugins():
    """PySide6 플랫폼 플러그인 경로를 반환 (Windows DLL 로딩 문제 해결)"""
    if sys.platform != 'win32':
        return []

    try:
        import PySide6
        pyside6_path = os.path.dirname(PySide6.__file__)
        plugins_path = os.path.join(pyside6_path, 'plugins')

        # 필요한 플러그인만 포함 (전체가 아닌 필수만)
        plugin_dirs = []
        required_plugins = ['platforms', 'styles', 'multimedia']  # 실제 필요한 것만

        for plugin in required_plugins:
            plugin_path = os.path.join(plugins_path, plugin)
            if os.path.exists(plugin_path):
                plugin_dirs.append((plugin_path, f'PySide6/plugins/{plugin}'))

        return plugin_dirs
    except:
        return []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/alert.wav', 'assets'),
        ('assets/fonts/Pretendard-Regular.otf', 'assets/fonts'),
        ('assets/fonts/Pretendard-Bold.otf', 'assets/fonts'),
    ] + get_pyside6_plugins(),  # Qt 플랫폼 플러그인 추가
    hiddenimports=[
        # PySide6 필수 모듈 (ui 폴더 전체에서 사용)
        'PySide6.QtCore',        # Signal, QTimer, QUrl, Qt 등
        'PySide6.QtWidgets',     # QWidget, QVBoxLayout, QLabel, QListWidget 등
        'PySide6.QtGui',         # QFont, QFontDatabase 등
        'PySide6.QtMultimedia',  # QSoundEffect (타이머 알림음)
        # Windows에서 필요한 내부 모듈
        'shiboken6',  # PySide6 C++ 바인딩 필수
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 불필요한 PySide6 모듈 제외
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        'PySide6.QtAxContainer',
        'PySide6.QtBluetooth',
        'PySide6.QtCharts',
        'PySide6.QtConcurrent',
        'PySide6.QtDataVisualization',
        'PySide6.QtDBus',
        'PySide6.QtDesigner',
        'PySide6.QtHelp',
        'PySide6.QtHttpServer',
        'PySide6.QtLocation',
        'PySide6.QtNetworkAuth',
        'PySide6.QtNfc',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtPdf',
        'PySide6.QtPdfWidgets',
        'PySide6.QtPositioning',
        'PySide6.QtPrintSupport',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtQuickControls2',
        'PySide6.QtQuickWidgets',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtSensors',
        'PySide6.QtSerialBus',
        'PySide6.QtSerialPort',
        'PySide6.QtSpatialAudio',
        'PySide6.QtSql',
        'PySide6.QtStateMachine',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        'PySide6.QtTest',
        'PySide6.QtTextToSpeech',
        'PySide6.QtUiTools',
        'PySide6.QtWebChannel',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineQuick',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebSockets',
        'PySide6.QtXml',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
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
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # PySide6 DLL 손상 방지를 위해 압축 비활성화
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/dasan.ico',
)
