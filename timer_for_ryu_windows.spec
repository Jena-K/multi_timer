# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# PySide6 경로 및 바이너리 찾기
def get_pyside6_info():
    """PySide6 설치 경로 및 바이너리 반환"""
    try:
        import PySide6
        pyside6_path = os.path.dirname(PySide6.__file__)

        # PySide6 바이너리 수집
        binaries = []
        for item in os.listdir(pyside6_path):
            item_path = os.path.join(pyside6_path, item)
            if item.endswith(('.dll', '.pyd', '.so', '.dylib')):
                binaries.append((item_path, 'PySide6'))

        return pyside6_path, binaries
    except Exception as e:
        print(f"PySide6 not found: {e}")
        return None, []

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

pyside6_path, pyside6_binaries = get_pyside6_info()
pathex_list = [pyside6_path] if pyside6_path else []

# PySide6 필수 모듈 수집
pyside6_modules = collect_submodules('PySide6.QtCore')
pyside6_modules += collect_submodules('PySide6.QtWidgets')
pyside6_modules += collect_submodules('PySide6.QtGui')
pyside6_modules += collect_submodules('PySide6.QtMultimedia')
pyside6_datas = collect_data_files('PySide6')

a = Analysis(
    ['main.py'],
    pathex=pathex_list,
    binaries=pyside6_binaries,
    datas=[
        ('assets/alert.wav', 'assets'),
        ('assets/fonts/Pretendard-Regular.otf', 'assets/fonts'),
        ('assets/fonts/Pretendard-Bold.otf', 'assets/fonts'),
    ] + get_pyside6_plugins() + pyside6_datas,
    hiddenimports=pyside6_modules + ['shiboken6'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
