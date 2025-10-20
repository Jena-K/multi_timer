# Windows .exe 빌드 가이드

## 🔧 크로스 플랫폼 렌더링 수정사항

### 해결된 문제들

1. **폰트 렌더링 문제**
   - Pretendard 폰트가 Windows에서 제대로 로드되지 않음
   - Pretendard 사용 불가시 Malgun Gothic으로 폴백
   - 폰트 힌팅 및 안티앨리어싱 설정 추가

2. **버튼 스타일 문제**
   - Windows가 플랫폼별 기본 버튼 스타일 적용
   - 배경색과 테두리가 올바르게 렌더링되지 않음
   - `setFlat(False)` 및 `setAutoFillBackground(False)` 사용으로 해결

3. **High DPI 스케일링**
   - DPI 속성을 QApplication 생성 **전**에 설정해야 함
   - Windows 디스플레이에 대한 적절한 스케일링 설정

### 기술적 변경사항

#### 1. main.py
- DPI 속성 설정을 QApplication 생성 전으로 이동
- 폰트 로딩 폴백 체인 강화:
  - Primary: Pretendard (커스텀 폰트)
  - Windows: Malgun Gothic
  - macOS: SF Pro Text
  - Linux: Noto Sans
- 폰트 힌팅 및 안티앨리어싱 설정 추가
- 전역 스타일시트에 font-family 폴백 적용

#### 2. ui/widgets/base_list_item.py
- 액션 버튼에 `setFlat(True)`를 `setFlat(False)`로 변경
- 올바른 렌더링을 위해 `setAutoFillBackground(False)` 추가
- 스타일시트에 명시적인 font-size 및 font-weight 추가

#### 3. ui/widgets/timer_list_item.py
- 컨트롤 버튼(재생/일시정지/정지)에 동일한 버튼 수정사항 적용
- 플랫폼 간 일관된 렌더링 보장

#### 4. ui/theme.py
- 모든 버튼 타입에 `:focus` 가상 클래스 스타일 추가
- Windows에서 일관된 포커스 동작 보장

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

## Windows 테스트 가이드

### 폰트 로딩 테스트

먼저 폰트가 제대로 로드되는지 확인:

```powershell
python test_font_loading.py
```

출력 예시:
```
[FONT] ✅ Successfully loaded: Pretendard-Regular.otf → ['Pretendard']
[FONT] ✅ Successfully loaded: Pretendard-Bold.otf → ['Pretendard']
```

- ✅ 표시가 나오면 폰트 로딩 성공
- ❌ 표시가 나오면 폰트 파일 경로 확인 필요
- ⚠️  표시가 나오면 파일이 없음

### 호환성 테스트 실행

```powershell
python test_windows_compatibility.py
```

테스트 창에서 확인할 사항:
- [ ] Pretendard 폰트가 올바르게 로드됨 (콘솔 출력 확인)
- [ ] Pretendard 실패 시 Malgun Gothic 폴백 사용
- [ ] Primary 버튼("+ 템플릿 추가")이 녹색 배경으로 표시
- [ ] 액션 버튼("수정", "삭제")이 회색 배경으로 표시
- [ ] 컨트롤 버튼(▶ ⏸ ⏹)이 올바른 색상으로 표시
- [ ] 한글 텍스트가 모든 UI 요소에서 올바르게 표시
- [ ] 버튼 호버 상태가 정상 작동
- [ ] High DPI 디스플레이에서 올바르게 렌더링

### 근본 원인 요약

#### 폰트 문제
**근본 원인**: 폰트 로딩이 QApplication 생성 후에 발생하며, Windows가 더 엄격한 폰트 렌더링 요구사항을 가짐

**해결책**:
- QApplication 직후 즉시 폰트 로딩
- 폰트 힌팅 설정 명시적으로 지정
- 포괄적인 폴백 체인 제공
- 일관된 font-family를 위한 전역 스타일시트 적용

#### 버튼 스타일 문제
**근본 원인**: Windows Qt 프레임워크가 CSS 스타일의 스타일시트를 무시하는 플랫폼별 네이티브 버튼 스타일 적용

**해결책**:
- 네이티브 스타일 방지를 위해 `setFlat(False)` 사용
- 스타일시트 배경 허용을 위해 `setAutoFillBackground(False)` 사용
- 스타일시트에 모든 폰트 속성을 명시적으로 지정 (family, size, weight)
- 일관된 상태 유지를 위해 `:focus` 가상 클래스 추가

#### High DPI 문제
**근본 원인**: QApplication 생성 후 설정된 DPI 속성이 Windows에서 제대로 적용되지 않음

**해결책**:
- QApplication 생성 **전**에 모든 DPI 속성 설정
- 더 나은 렌더링을 위해 `setHintingPreference` 및 `setStyleStrategy` 사용

## 빌드 성공 체크리스트

- [ ] Timer For Ryu.exe 프로세스 종료
- [ ] dist/build 폴더 삭제 (선택)
- [ ] assets/dasan.ico 파일 존재 확인
- [ ] PyInstaller 설치 확인
- [ ] 빌드 명령 실행
- [ ] dist 폴더에서 .exe 파일 확인
- [ ] .exe 실행 테스트
- [ ] 호환성 테스트 스크립트 실행
- [ ] 폰트 렌더링 확인
- [ ] 버튼 스타일 확인
