# 한눈영양 🥗

## 1. 서비스 소개

**한눈영양**은 식품의 영양성분을 입력하면 AI가 어려운 영양 정보를 쉽게 설명해주는 웹 서비스입니다.

영양성분표를 봐도 당류, 나트륨, 지방 등이 많은지 적은지 바로 이해하기 어려운 사람을 위해 만들었습니다.

사용자는 제품 정보와 영양성분을 입력하고 **AI 분석하기** 버튼을 누르면, AI가 다음 내용을 쉽게 설명해줍니다.

- 전체적인 영양 특징
- 주의할 점
- 먹어보는 방법
- 비교해볼 만한 대체 식품

> 본 서비스의 AI 결과는 일반적인 영양 정보 참고용이며 의료적 진단이나 치료를 대신하지 않습니다.

## 2. 주요 대상

- 영양성분표를 어렵게 느끼는 일반 사용자
- 간식이나 음료를 고를 때 영양 정보를 비교하고 싶은 사람
- 건강한 식품 선택을 쉽게 하고 싶은 사람

## 3. 주요 기능

### ① 홈
서비스의 목적과 사용 방법을 소개합니다.

### ② AI 라벨 분석
제품명, 제품 유형, 영양성분을 입력하면 Gemini AI가 분석 결과를 보여줍니다.

### ③ 건강 정보 / 서비스 소개 영역
영양 정보를 이해하는 데 도움을 주는 내용과 서비스 설명을 제공합니다.

## 4. 기술 스택

### Frontend
- HTML
- CSS
- JavaScript
- 별도의 프레임워크 없이 순수 HTML/CSS/JavaScript 사용

### Backend
- Python
- Vercel Serverless Functions
- FastAPI

### AI
- Google Gemini API
- `gemini-3.6-flash`

### 배포 / 버전 관리
- GitHub
- Vercel

## 5. 프로젝트 구조

```text
AI_Nutrition_Label/
├── api/
│   └── index.py          # Python API / AI 분석
├── css/
│   └── style.css         # 화면 디자인
├── js/
│   └── app.js            # 버튼, 입력, API 요청 처리
├── index.html             # 메인 화면
├── pyproject.toml         # Python 프로젝트 및 패키지 설정
├── requirements.txt       # Python 패키지 목록
├── README.md              # 프로젝트 설명
└── .gitignore             # 비밀 파일 보호
```

## 6. 동작 흐름

```text
사용자 입력
   ↓
JavaScript(app.js)
   ↓ fetch('/api')
Vercel Python API(api/index.py)
   ↓
Gemini API
   ↓
AI 분석 결과
   ↓
웹 화면에 결과 표시
```

## 7. 환경 변수 설정

API 키는 코드에 직접 쓰지 않고 환경 변수로 관리합니다.

필요한 환경 변수:

```text
GEMINI_API_KEY=내_Gemini_API_키
```

로컬 개발에서는 프로젝트의 `.env` 파일에 저장하고, `.env`는 GitHub에 올리지 않습니다.

Vercel에서는 **Project → Settings → Environment Variables**에 `GEMINI_API_KEY`를 등록합니다.

> 실제 API 키는 README, GitHub, 코드, 발표 자료, 스크린샷에 공개하지 않습니다.

## 8. 로컬 실행 방법

### 1) 저장소 받기

```bash
git clone https://github.com/KIMDABHIN/codyssey_A1-3.git
cd codyssey_A1-3
```

### 2) 패키지 설치

```bash
python -m pip install -r requirements.txt
```

필요한 경우:

```bash
python -m pip install fastapi google-genai python-dotenv
```

### 3) 환경 변수 설정

`.env` 파일에 `GEMINI_API_KEY`를 설정합니다.

### 4) 배포는 GitHub와 Vercel을 연결하여 진행합니다.

## 9. 배포 URL
https://codyssey-a1-3-woad.vercel.app/

## 10. 오류를 해결하면서 배운 점

개발 과정에서 여러 오류를 직접 확인하고 수정했습니다.

- GitHub 인증이 다른 계정으로 잡혀 `403` 오류가 발생했으며 Windows 자격 증명을 정리한 뒤 다시 인증했습니다.
- Vercel에서 Python 엔트리포인트 문제를 확인했습니다.
- `pyproject.toml` 설정 문제를 확인했습니다.
- 정적 파일과 Python API를 함께 제공하는 구조를 조정했습니다.
- `app.js`에 Markdown 코드 표시가 실제로 들어가 JavaScript 오류가 발생한 것을 확인하고 수정했습니다.
- Gemini API 요청에서 `gemini-2.5-flash`가 신규 사용자에게 제공되지 않아 `404 NOT_FOUND`가 발생한 것을 확인했습니다.
- 실제 로컬 API 호출로 문제를 재현한 뒤 사용 가능한 `gemini-3.6-flash`로 변경했습니다.
- 마지막에는 Vercel 로그에서 `POST /api 200`을 확인하고 AI 분석 결과가 실제 화면에 표시되는 것을 확인했습니다.

## 11. GitHub

https://github.com/KIMDABHIN/codyssey_A1-3
