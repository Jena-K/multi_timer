# SVG 아이콘 솔루션 - 크로스 플랫폼 일관성

## 🎯 문제 분석

### 문제: Windows에서 컨트롤 버튼이 늘어져 보임

**증상**:
- macOS: 컨트롤 버튼(►❚❚■)이 정사각형으로 보임
- Windows: 같은 버튼이 가로로 늘어나 직사각형으로 보임

**근본 원인**:

1. **폰트 렌더링 차이**
   - 유니코드 기호는 시스템 폰트에 의존
   - Windows: Segoe UI Symbol, Segoe UI Emoji
   - macOS: Apple Color Emoji, SF Pro
   - 각 폰트의 glyph 너비(advance width)가 다름

2. **폰트 메트릭 불일치**
   - 같은 유니코드 포인트(U+25BA)라도 플랫폼별로 다른 비율
   - 버튼 크기는 50x50 고정이지만 내부 텍스트는 폰트에 따라 늘어남

3. **Fallback 폰트 체인**
   - Pretendard는 이모지/기호 미포함
   - 시스템이 자동으로 fallback 폰트 선택
   - Windows와 macOS의 fallback 로직이 다름

## ✅ 해결 방법: SVG 아이콘

### 왜 SVG인가?

1. **완벽한 크로스 플랫폼 일관성**
   - 벡터 그래픽 → 모든 플랫폼에서 동일한 렌더링
   - 폰트에 의존하지 않음

2. **완벽한 비율 제어**
   - viewBox로 정확한 aspect ratio 지정
   - 어떤 크기든 동일한 비율 유지

3. **색상 자유도**
   - SVG의 `fill="currentColor"` 속성 활용
   - 프로그래밍으로 색상 변경 가능
   - hover/pressed 상태별 다른 색상

4. **고해상도 지원**
   - 벡터이므로 어떤 DPI에서도 선명함
   - Retina/4K 디스플레이 완벽 지원

## 📁 구현 내용

### 1. SVG 아이콘 파일

**assets/icons/play.svg**:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M8 5v14l11-7z"/>
</svg>
```

**assets/icons/pause.svg**:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
</svg>
```

**assets/icons/stop.svg**:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M6 6h12v12H6z"/>
</svg>
```

**특징**:
- `viewBox="0 0 24 24"`: 24x24 정사각형 비율
- `fill="currentColor"`: 프로그래밍으로 색상 변경 가능
- 간결한 path 데이터

### 2. SVG 아이콘 로더

**ui/utils/icon_loader.py**:

```python
def create_svg_icon(icon_name: str, color: str, size: int = 24) -> QIcon:
    """
    Create a QIcon from an SVG file with specified color.

    1. SVG 파일 읽기
    2. currentColor를 실제 색상으로 치환
    3. QSvgRenderer로 렌더링
    4. QPixmap 생성 (투명 배경)
    5. QIcon 반환
    """
```

**기능**:
- PyInstaller 번들 모드 지원 (`sys._MEIPASS`)
- 색상 동적 변경
- 크기 조절 (기본 24px)

### 3. 버튼 생성 로직

**ui/widgets/timer_list_item.py**:

```python
def _create_control_button_with_icon(self, icon_name, color, hover, pressed):
    btn = QPushButton()
    btn.setIconSize(QSize(30, 30))  # 정확한 크기 지정

    # 색상 정보를 버튼 프로퍼티에 저장
    btn.setProperty("color_normal", color)
    btn.setProperty("color_hover", hover)
    btn.setProperty("color_pressed", pressed)

    # Event filter로 hover/pressed 상태 처리
    btn.installEventFilter(self)
```

### 4. 상호작용 처리

**eventFilter 메서드**:

```python
def eventFilter(self, obj, event):
    if event.type() == QEvent.Type.Enter:
        # Hover: 아이콘을 hover 색상으로 재생성
        icon = create_svg_icon(icon_name, color_hover, icon_size)
        obj.setIcon(icon)

    elif event.type() == QEvent.Type.Leave:
        # Normal: 원래 색상으로 복구
        icon = create_svg_icon(icon_name, color_normal, icon_size)
        obj.setIcon(icon)
```

## 🔧 기술적 세부사항

### SVG → QIcon 변환 과정

1. **SVG 파일 읽기**
   ```python
   with open(icon_path, 'r') as f:
       svg_data = f.read()
   ```

2. **색상 치환**
   ```python
   svg_data = svg_data.replace('currentColor', '#43a047')
   ```

3. **QSvgRenderer 생성**
   ```python
   renderer = QSvgRenderer(svg_data.encode('utf-8'))
   ```

4. **QPixmap 렌더링**
   ```python
   pixmap = QPixmap(QSize(30, 30))
   pixmap.fill(QColor(0, 0, 0, 0))  # 투명
   painter = QPainter(pixmap)
   renderer.render(painter)
   ```

5. **QIcon 생성**
   ```python
   icon = QIcon(pixmap)
   ```

### 왜 텍스트가 아닌 아이콘인가?

**텍스트 (유니코드) 방식**:
```python
btn = QPushButton("►")  # 폰트에 의존
```
- ❌ 플랫폼별 폰트 차이
- ❌ 비율 제어 불가
- ❌ 고해상도 대응 미흡

**아이콘 (SVG) 방식**:
```python
btn.setIcon(create_svg_icon("play.svg", "#43a047", 30))
```
- ✅ 플랫폼 무관
- ✅ 정확한 비율 보장
- ✅ 완벽한 고해상도 지원

## 📦 PyInstaller 설정

**timer_for_ryu_windows.spec**:

```python
datas=[
    ('assets/fonts', 'assets/fonts'),
    ('assets/icons', 'assets/icons'),  # SVG 아이콘 포함
],
hiddenimports=[
    'PySide6.QtSvg',  # SVG 렌더링 필수
],
```

## ✨ 결과

### Before (유니코드 기호)
- macOS: 정사각형 ✅
- Windows: 가로로 늘어남 ❌
- 폰트에 따라 다름 ❌

### After (SVG 아이콘)
- macOS: 정사각형 ✅
- Windows: 정사각형 ✅
- 모든 플랫폼 동일 ✅

## 🎨 디자인 가이드라인

### SVG 아이콘 제작 시 주의사항

1. **viewBox 사용**
   - 항상 정사각형 (예: `0 0 24 24`)
   - 비율 일관성 보장

2. **fill="currentColor"**
   - 프로그래밍으로 색상 변경 가능
   - 다크모드 대응 용이

3. **경로 최적화**
   - 간결한 path 데이터
   - 파일 크기 최소화

4. **stroke 대신 fill**
   - 스케일링 시 선 굵기 문제 없음
   - 렌더링 성능 향상

### 권장 사이즈

- **버튼 크기**: 50x50px
- **아이콘 크기**: 30x30px (60% 비율)
- **SVG viewBox**: 24x24 (표준)

## 🧪 테스트

### macOS에서 테스트
```bash
uv run python main.py
```

### Windows에서 테스트
```powershell
python main.py
```

### 확인 사항
- [ ] 컨트롤 버튼이 정사각형으로 보임
- [ ] hover 시 색상 변경 작동
- [ ] pressed 시 색상 변경 작동
- [ ] 모든 플랫폼에서 동일한 비율

---

**작성일**: 2025-10-20
**버전**: 1.0.0
**작성자**: rowan@lionrocket.ai
