# Windows 크로스 플랫폼 렌더링 수정사항 요약

## 문제 분석

macOS에서 정상 작동하던 UI가 Windows에서 다르게 렌더링되는 문제가 발생했습니다:

1. **폰트 문제**: Pretendard 폰트가 Windows에서 제대로 적용되지 않음
2. **버튼 스타일 문제**: 버튼 배경색과 디자인이 제대로 적용되지 않음
3. **전반적인 UI 일관성**: Windows 네이티브 스타일이 커스텀 스타일을 무시

## 근본 원인

### 1. 폰트 렌더링 문제
- **원인**: Windows는 macOS보다 폰트 로딩과 렌더링에 더 엄격한 요구사항이 있음
- **증상**: Pretendard 폰트가 로드되지 않거나 시스템 기본 폰트로 대체됨

### 2. 버튼 스타일 문제
- **원인**: Windows Qt는 플랫폼별 네이티브 버튼 스타일을 기본으로 적용하며, 이것이 QSS(Qt Style Sheet)를 무시함
- **증상**:
  - 녹색 "템플릿 추가" 버튼이 기본 회색 버튼으로 표시
  - 회색 "수정/삭제" 버튼의 배경색이 적용되지 않음
  - 컨트롤 버튼(▶⏸⏹)의 색상이 제대로 표시되지 않음

### 3. High DPI 스케일링
- **원인**: DPI 관련 속성이 QApplication 생성 후에 설정되면 Windows에서 무시됨
- **증상**: 고해상도 디스플레이에서 UI 요소가 흐릿하거나 크기가 잘못됨

## 해결 방법

### 파일별 수정사항

#### 1. main.py
```python
# 변경 전: DPI 설정이 QApplication 생성 후
app = QApplication(sys.argv)
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

# 변경 후: DPI 설정을 QApplication 생성 전으로 이동
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
```

**추가 개선사항**:
- 폰트 폴백 체인 강화 (Pretendard → Malgun Gothic → SF Pro Text → Noto Sans)
- QFont에 힌팅과 안티앨리어싱 설정 추가
- 전역 스타일시트로 font-family 일관성 보장

```python
default_font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
default_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
app.setFont(default_font)

platform_stylesheet = """
    * {
        font-family: "Pretendard", "Malgun Gothic", "Microsoft YaHei", "SF Pro Text", system-ui, sans-serif;
    }
"""
app.setStyleSheet(platform_stylesheet)
```

#### 2. ui/widgets/base_list_item.py
```python
# 변경 전: Windows에서 작동하지 않음
btn.setFlat(True)

# 변경 후: Windows에서 제대로 작동
btn.setFlat(False)
btn.setAutoFillBackground(False)
```

**스타일시트 개선**:
```python
# font-size와 font-weight를 명시적으로 추가
btn.setStyleSheet(f"""
    QPushButton {{
        ...
        font-family: {Theme.Fonts.FAMILY_FALLBACK};
        font-size: {Theme.Fonts.SIZE_SMALL}px;
        font-weight: bold;
    }}
""")
```

#### 3. ui/widgets/timer_list_item.py
- base_list_item.py와 동일한 변경사항을 컨트롤 버튼에 적용
- `setFlat(False)` 및 `setAutoFillBackground(False)` 추가

#### 4. ui/theme.py
- 모든 버튼 스타일에 `:focus` 상태 추가
- Windows에서 포커스 시 일관된 스타일 보장

```python
QPushButton:focus {{
    outline: none;
    border: none;
}}
```

## 기술적 세부사항

### setFlat() 동작 방식

- **setFlat(True)**:
  - macOS: QSS 스타일이 정상 적용됨
  - Windows: 네이티브 플랫폼 스타일이 QSS를 무시함

- **setFlat(False)**:
  - 모든 플랫폼에서 QSS 스타일이 정상 적용됨
  - `setAutoFillBackground(False)`와 함께 사용하여 배경색 제어

### 폰트 로딩 순서

1. `load_fonts()` - Pretendard OTF 파일 로드
2. QFontDatabase에서 사용 가능한 폰트 확인
3. 플랫폼별 폴백 폰트 선택
4. QFont 객체 생성 및 힌팅 설정
5. 애플리케이션 기본 폰트로 설정
6. 전역 스타일시트로 폰트 패밀리 적용

### DPI 스케일링 순서

```python
# 1. QApplication 생성 전 속성 설정 (중요!)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# 2. QApplication 생성
app = QApplication(sys.argv)

# 3. 스케일링 정책 설정
QApplication.setHighDpiScaleFactorRoundingPolicy(...)
```

## 테스트 방법

### macOS에서 테스트
```bash
uv run python main.py
uv run python test_windows_compatibility.py
```

### Windows에서 테스트
```powershell
python main.py
python test_windows_compatibility.py
```

### 확인 사항
- [ ] Pretendard 폰트 로딩 확인 (콘솔 출력)
- [ ] "템플릿 추가" 버튼이 녹색 배경
- [ ] "수정/삭제" 버튼이 회색 배경
- [ ] 컨트롤 버튼이 올바른 색상 표시
- [ ] 한글 폰트가 깔끔하게 렌더링
- [ ] 버튼 호버 효과 작동
- [ ] High DPI 디스플레이에서 선명함

## 빌드 방법

Windows에서 실행 파일 생성:
```powershell
pyinstaller --clean --noconfirm timer_for_ryu_windows.spec
```

자세한 내용은 [BUILD_WINDOWS.md](BUILD_WINDOWS.md) 참조

## 참고사항

- 이 수정사항은 macOS, Windows, Linux 모두에서 작동합니다
- 기존 macOS 동작에는 영향을 주지 않습니다
- PyInstaller spec 파일에 폰트 파일이 포함되어 있어야 합니다
- Windows 사용자는 빌드된 .exe 파일만 실행하면 됩니다

## 문제 해결

### 폰트가 여전히 로드되지 않는 경우
1. `assets/fonts/` 폴더에 Pretendard 파일 확인
2. PyInstaller spec의 `datas` 섹션 확인
3. 콘솔 출력에서 폰트 로딩 메시지 확인

### 버튼 스타일이 여전히 적용되지 않는 경우
1. `setFlat(False)` 사용 확인
2. `setAutoFillBackground(False)` 호출 확인
3. 스타일시트에 `font-size`와 `font-weight` 포함 확인

### High DPI 문제가 계속되는 경우
1. DPI 속성이 QApplication 생성 **전**에 설정되었는지 확인
2. Windows 디스플레이 설정 확인 (125%, 150%, 200%)
3. Qt 버전이 최신인지 확인 (PySide6 6.5+)

---

**작성일**: 2025-10-20
**버전**: 1.0.0
**작성자**: rowan@lionrocket.ai
