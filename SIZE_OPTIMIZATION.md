# Windows 실행 파일 크기 최적화 가이드

## 📊 크기 분석

### PySide6 기본 크기

PySide6는 Qt 프레임워크의 Python 바인딩으로, 기본적으로 매우 큽니다:

| 구성 요소 | 크기 |
|----------|------|
| Qt6Core.dll | ~6-8 MB |
| Qt6Gui.dll | ~6-8 MB |
| Qt6Widgets.dll | ~4-6 MB |
| Qt6Multimedia.dll | ~2-3 MB |
| Qt6Svg.dll | ~1-2 MB |
| Python 런타임 | ~10-15 MB |
| 기타 의존성 | ~10-20 MB |
| **총합** | **~40-60 MB** |

## ✅ 적용된 최적화

### 1. 불필요한 Qt 모듈 제외

**timer_for_ryu_windows.spec**에서 사용하지 않는 PySide6 모듈 제외:

```python
excludes=[
    # 웹 관련 (큼)
    'PySide6.QtWebEngine',      # ~100 MB
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebChannel',
    'PySide6.QtWebSockets',

    # 3D 관련 (큼)
    'PySide6.Qt3DAnimation',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DExtras',
    'PySide6.Qt3DInput',
    'PySide6.Qt3DLogic',
    'PySide6.Qt3DRender',

    # QML/Quick (중간)
    'PySide6.QtQml',
    'PySide6.QtQuick',
    'PySide6.QtQuick3D',

    # 데이터베이스
    'PySide6.QtSql',

    # 기타
    'PySide6.QtNetwork',
    'PySide6.QtBluetooth',
    'PySide6.QtLocation',
    'PySide6.QtPrintSupport',
    # ... 등 25개 이상
]
```

**예상 절감**: ~30-50% (15-25 MB)

### 2. Python 패키지 제외

불필요한 Python 라이브러리 제외:

```python
excludes=[
    # 과학 계산 (매우 큼)
    'numpy',        # ~20 MB
    'scipy',        # ~40 MB
    'pandas',       # ~30 MB
    'matplotlib',   # ~40 MB

    # 개발 도구
    'IPython',
    'jupyter',
    'pytest',
    'unittest',

    # GUI 프레임워크
    'tkinter',
]
```

**예상 절감**: ~100+ MB (이미 설치 안 했다면 효과 없음)

### 3. UPX 압축

**UPX (Ultimate Packer for eXecutables)** 활성화:

```python
exe = EXE(
    ...
    strip=True,       # 디버그 심볼 제거
    upx=True,         # UPX 압축 활성화
    upx_exclude=[     # Qt DLL은 압축 제외 (손상 방지)
        'Qt6Core.dll',
        'Qt6Gui.dll',
        'Qt6Widgets.dll',
        'Qt6Multimedia.dll',
        'Qt6Svg.dll',
    ],
)
```

**예상 절감**: ~30-40% 추가 압축

**주의사항**:
- UPX는 실행 시 압축 해제 필요 (첫 실행 시 약간 느림)
- Qt DLL 압축 시 손상 가능 → exclude 목록 사용
- 일부 안티바이러스가 UPX 압축 파일을 의심할 수 있음

### 4. Strip 심볼

```python
strip=True
```

디버그 심볼과 불필요한 메타데이터 제거

**예상 절감**: ~5-10%

## 📉 최종 예상 크기

### Before (최적화 전)
```
기본 PySide6 앱: ~60-80 MB
```

### After (최적화 후)
```
exclude 적용: ~40-50 MB  (30% 감소)
UPX 압축 추가: ~25-35 MB  (40% 추가 감소)
```

### 최종 예상 크기: **25-35 MB**

## 🔧 추가 최적화 방법

### 방법 1: 폴더 배포 방식

**현재**: `--onefile` (단일 파일)
**대안**: `--onedir` (폴더 방식)

```python
# .spec 파일에서 EXE 대신 COLLECT 사용
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=['Qt6*.dll'],
    name='Timer For Ryu'
)
```

**장점**:
- 압축 해제 불필요 → 빠른 시작
- 개별 DLL 업데이트 가능
- 더 나은 UPX 압축률

**단점**:
- 여러 파일로 배포
- 사용자가 폴더 전체 관리 필요

**예상 크기**: 폴더 전체 ~20-30 MB

### 방법 2: 최소 Qt 빌드 사용

PySide6 대신 경량 GUI 프레임워크 고려:

| 프레임워크 | 크기 | 기능 |
|-----------|------|------|
| PySide6 | 40-60 MB | 완전한 Qt |
| PyQt5-slim | 30-40 MB | Qt 기본 기능 |
| tkinter | ~5 MB | Python 기본 GUI |
| PySimpleGUI | ~10 MB | 간단한 GUI |
| wxPython | 20-30 MB | 네이티브 위젯 |

**현재 프로젝트**: PySide6 사용 권장 (이미 구현됨)

### 방법 3: 7-Zip SFX 압축

빌드 후 추가로 7-Zip SFX(자동 압축 해제)로 패키징:

```bash
# Windows에서
7z a -t7z -m0=lzma2 -mx=9 Timer.7z "Timer For Ryu.exe"
copy /b 7zS.sfx + config.txt + Timer.7z "Timer For Ryu (Compressed).exe"
```

**예상 절감**: ~20-30% 추가

**총 크기**: ~18-25 MB

**단점**:
- 첫 실행 시 압축 해제 필요
- 임시 폴더 사용
- 일부 안티바이러스 경고

## 🧪 크기 측정 방법

### 빌드 전 분석

```powershell
# PyInstaller 분석 모드
pyinstaller --clean --log-level DEBUG timer_for_ryu_windows.spec

# 빌드 로그 확인
# Build analysis 섹션에서 포함된 모듈 확인
```

### 빌드 후 확인

```powershell
# 파일 크기 확인
dir "dist\Timer For Ryu.exe"

# 폴더 방식인 경우 전체 크기
Get-ChildItem -Path "dist\Timer For Ryu" -Recurse |
    Measure-Object -Property Length -Sum

# 각 DLL 크기 확인
Get-ChildItem -Path "dist\Timer For Ryu" -Filter "*.dll" |
    Sort-Object Length -Descending |
    Format-Table Name, @{Label="Size (MB)"; Expression={$_.Length / 1MB}}
```

## 🚀 권장 빌드 명령

### 개발/디버그용 (빠른 빌드)
```powershell
pyinstaller --clean --noconfirm timer_for_ryu_windows.spec
```

### 배포용 (최소 크기)
```powershell
# 1. 먼저 UPX 설치 (Windows)
# https://github.com/upx/upx/releases
# upx.exe를 PATH에 추가

# 2. 빌드
pyinstaller --clean --noconfirm timer_for_ryu_windows.spec

# 3. 크기 확인
dir "dist\Timer For Ryu.exe"
```

## 📋 빌드 체크리스트

배포용 빌드 전 확인사항:

- [ ] `.spec` 파일에서 `console=False` 설정
- [ ] `upx=True` 활성화
- [ ] `strip=True` 활성화
- [ ] 불필요한 `excludes` 확인
- [ ] UPX 설치 확인 (`upx --version`)
- [ ] 빌드 후 실행 테스트
- [ ] 파일 크기 확인

## ⚠️ 주의사항

### UPX 관련

1. **안티바이러스 경고**
   - 일부 안티바이러스가 UPX 압축 파일을 의심
   - 배포 전 VirusTotal 등에서 확인
   - 코드 서명 인증서 사용 권장

2. **실행 속도**
   - UPX 압축 시 첫 실행이 약간 느림
   - 이후 실행은 정상 속도
   - SSD에서는 거의 차이 없음

3. **Qt DLL**
   - Qt DLL을 UPX 압축하면 손상 가능
   - `upx_exclude` 목록에 반드시 포함

### 크기 vs 성능

| 설정 | 크기 | 시작 속도 | 안정성 |
|------|------|----------|--------|
| 최소 최적화 | 60 MB | 빠름 | 높음 |
| 권장 설정 | 30 MB | 보통 | 높음 |
| 극한 압축 | 20 MB | 느림 | 중간 |

**권장**: UPX + excludes (30 MB 목표)

## 📊 실제 측정 결과 (예상)

```
Before:
- 최적화 전: ~65 MB

After:
- excludes만: ~45 MB (31% 감소)
- excludes + UPX: ~28 MB (57% 감소)
- + 7-Zip SFX: ~20 MB (69% 감소)
```

---

**작성일**: 2025-10-20
**버전**: 1.0.0
**작성자**: rowan@lionrocket.ai
