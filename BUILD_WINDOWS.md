# Windows .exe 빌드 가이드

## 🚨 중요: ModuleNotFoundError 'PySide6' 해결

PySide6를 사용하는 경우 반드시 `--collect-all PySide6` 옵션을 추가하세요!

## 0. 빌드 전 필수 사항 ⚠️

### PermissionError 방지

빌드 전에 반드시:
1. **기존 Timer For Ryu.exe 프로세스 종료**
   - 작업 관리자 (Ctrl+Shift+Esc) 열기
   - "Timer For Ryu.exe" 프로세스 찾아서 강제 종료
   - 또는 PowerShell에서:
   ```powershell
   taskkill /F /IM "Timer For Ryu.exe"
   ```

2. **dist 폴더 수동 삭제** (선택사항, 권장)
   ```powershell
   Remove-Item -Recurse -Force dist
   Remove-Item -Recurse -Force build
   ```

3. **안티바이러스 제외 설정** (필요시)
   - Windows Defender가 .exe 파일 접근을 차단할 수 있음
   - 프로젝트 폴더를 제외 목록에 추가

## 1. 필수 패키지 설치

```powershell
pip install pyinstaller pillow
```

## 2. 아이콘 변환 (선택사항)

```powershell
python convert_icon.py
```

이 명령어는 `assets/dasan.png`를 `assets/dasan.ico`로 변환합니다.

## 3. .exe 파일 생성

### ✅ 방법 1: .spec 파일 사용 (가장 안정적, 권장)

```powershell
pyinstaller --clean --noconfirm timer_for_ryu_windows.spec
```

이 방법이 **가장 권장**됩니다. PySide6 모듈이 자동으로 포함됩니다.

### 방법 2: PowerShell에서 명령줄 빌드

```powershell
pyinstaller --onefile --windowed --name "Timer For Ryu" `
  --add-data "assets\alert.wav;assets" `
  --add-data "assets\fonts;assets\fonts" `
  --hidden-import PySide6.QtCore `
  --hidden-import PySide6.QtWidgets `
  --hidden-import PySide6.QtGui `
  --hidden-import PySide6.QtMultimedia `
  --collect-all PySide6 `
  --icon="assets\dasan.ico" `
  main.py
```

**주의**: PowerShell에서는 줄 연결에 백틱(`)을 사용합니다.

### 방법 3: CMD에서 빌드

```cmd
pyinstaller --onefile --windowed --name "Timer For Ryu" ^
  --add-data "assets\alert.wav;assets" ^
  --add-data "assets\fonts;assets\fonts" ^
  --hidden-import PySide6.QtCore ^
  --hidden-import PySide6.QtWidgets ^
  --hidden-import PySide6.QtGui ^
  --hidden-import PySide6.QtMultimedia ^
  --collect-all PySide6 ^
  --icon="assets\dasan.ico" ^
  main.py
```

**주의**: CMD에서는 줄 연결에 캐럿(^)을 사용합니다.

## 4. 결과물 확인

- **단일 파일**: `dist\Timer For Ryu.exe`
- **폴더 형태**: `dist\Timer For Ryu\Timer For Ryu.exe`

## 5. 실행 테스트

```powershell
cd dist
.\Timer` For` Ryu.exe
```

또는

```powershell
& "dist\Timer For Ryu.exe"
```

## 옵션 설명

- `--onefile`: 모든 파일을 하나의 .exe로 패키징
- `--windowed`: 콘솔 창 숨기기 (GUI 앱)
- `--name`: 실행 파일 이름
- `--add-data`: 리소스 파일 포함 (Windows: `source;destination`)
- `--icon`: 아이콘 파일 (.ico)
- `--hidden-import`: 명시적 모듈 import
- `--collect-all PySide6`: PySide6 모든 파일 포함 (**필수**)
- `--clean`: 이전 빌드 캐시 제거
- `--noconfirm`: 덮어쓰기 확인 없이 진행

## 트러블슈팅

### ❌ PermissionError: [WinError 5] 액세스가 거부되었습니다

**원인**: 기존 .exe 파일이 실행 중이거나 다른 프로세스가 사용 중

**해결**:
1. **프로세스 강제 종료**
   ```powershell
   taskkill /F /IM "Timer For Ryu.exe"
   ```

2. **dist/build 폴더 삭제 후 재시도**
   ```powershell
   Remove-Item -Recurse -Force dist, build
   pyinstaller --clean --noconfirm timer_for_ryu_windows.spec
   ```

3. **관리자 권한으로 PowerShell 실행**
   - PowerShell 우클릭 → "관리자 권한으로 실행"

4. **Windows Defender 제외 설정**
   - Windows 보안 → 바이러스 및 위협 방지 → 설정 관리
   - 제외 → 제외 추가 → 폴더
   - 프로젝트 폴더 선택

### ❌ ModuleNotFoundError: No module named 'PySide6'

**원인**: PySide6가 제대로 포함되지 않음

**해결**:
1. `.spec` 파일 사용 (권장)
2. `--collect-all PySide6` 옵션 추가
3. `--hidden-import` 옵션들 추가

### 폰트가 로드되지 않는 경우
- `assets/fonts` 폴더가 제대로 포함되었는지 확인
- `--add-data "assets\fonts;assets\fonts"` 옵션 추가

### 알림 소리가 재생되지 않는 경우
- `assets/alert.wav` 파일이 포함되었는지 확인
- `--add-data "assets\alert.wav;assets"` 옵션 추가

### 아이콘이 표시되지 않는 경우
- `assets/dasan.ico` 파일이 생성되었는지 확인
- `convert_icon.py` 스크립트를 먼저 실행

### UPX 압축 오류가 발생하는 경우
- `--upx-exclude` 옵션 추가 또는
- .spec 파일에서 `upx=False`로 설정

## 빌드 성공 체크리스트

- [ ] Timer For Ryu.exe 프로세스 종료
- [ ] dist/build 폴더 삭제 (선택)
- [ ] assets/dasan.ico 파일 존재 확인
- [ ] PyInstaller 설치 확인
- [ ] 빌드 명령 실행
- [ ] dist 폴더에서 .exe 파일 확인
- [ ] .exe 실행 테스트
