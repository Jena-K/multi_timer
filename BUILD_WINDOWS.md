# Windows .exe 빌드 가이드

## 1. 필수 패키지 설치

```bash
uv pip install pyinstaller pillow
```

## 2. 아이콘 변환 (PNG → ICO)

```bash
uv run python convert_icon.py
```

이 명령어는 `assets/dasan.png`를 `assets/dasan.ico`로 변환합니다.

## 3. .exe 파일 생성

### 방법 1: 단일 .exe 파일 (권장)

```bash
pyinstaller --onefile --windowed --name "Timer For Ryu" --add-data "assets/alert.wav;assets" --add-data "assets/fonts;assets/fonts" --icon="assets/dasan.ico" main.py
```

### 방법 2: 폴더 형태 (빠른 실행)

```bash
pyinstaller --windowed --name "Timer For Ryu" --add-data "assets/alert.wav;assets" --add-data "assets/fonts;assets/fonts" --icon="assets/dasan.ico" main.py
```

### 방법 3: .spec 파일 수정 후 빌드

1. `Timer For Ryu.spec` 파일 수정:
   - `datas=[...]` 부분에 폰트 추가
   - `icon='assets/dasan.ico'` 추가

2. 빌드 실행:
```bash
pyinstaller --clean --noconfirm "Timer For Ryu.spec"
```

## 4. 결과물 확인

- **단일 파일**: `dist/Timer For Ryu.exe`
- **폴더 형태**: `dist/Timer For Ryu/Timer For Ryu.exe`

## 5. 실행 테스트

```bash
cd dist
"Timer For Ryu.exe"
```

## 옵션 설명

- `--onefile`: 모든 파일을 하나의 .exe로 패키징
- `--windowed`: 콘솔 창 숨기기 (GUI 앱)
- `--name`: 실행 파일 이름
- `--add-data`: 리소스 파일 포함 (형식: `source;destination`)
- `--icon`: 아이콘 파일 (.ico)
- `--clean`: 이전 빌드 캐시 제거
- `--noconfirm`: 덮어쓰기 확인 없이 진행

## 트러블슈팅

### 폰트가 로드되지 않는 경우
- `assets/fonts` 폴더가 제대로 포함되었는지 확인
- `--add-data "assets/fonts;assets/fonts"` 옵션 추가

### 알림 소리가 재생되지 않는 경우
- `assets/alert.wav` 파일이 포함되었는지 확인
- `--add-data "assets/alert.wav;assets"` 옵션 추가

### 아이콘이 표시되지 않는 경우
- `assets/dasan.ico` 파일이 생성되었는지 확인
- `convert_icon.py` 스크립트를 먼저 실행
