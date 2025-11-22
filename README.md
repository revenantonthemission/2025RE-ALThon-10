# 강의 시뮬레이터

> Gemini AI 기반 개인화된 강의 분석 및 추천 시스템

## 프로젝트 개요

강의 시뮬레이터는 학생들의 수강 이력, 성적, 학습 선호도를 기반으로 특정 강의의 적합성을 분석하고 예측하는 AI 기반 플랫폼입니다. Gemini API를 활용하여 개인화된 강의 평가와 위험도 분석을 제공합니다.

## 주요 기능

### 개인화된 강의 분석
- 수강 이력 및 성적 기반 학습 적합도 평가
- 평가 방식 선호도 분석 (시험 vs 과제)
- 팀 프로젝트 선호도 고려
- 출석 방식 선호도 반영 (온라인/오프라인/하이브리드)

### AI 기반 평가
- Gemini AI를 활용한 종합적인 강의 적합도 분석
- 다차원 평가 기준 (학습 적합도, 평가 방식, 팀 프로젝트 등)
- 상세한 근거 제공
- 개인화된 요약 및 추천

### 강의 데이터베이스
- PostgreSQL 기반 강의 정보 관리
- 벡터 검색을 통한 유사 강의 추천
- Excel 데이터 자동 임포트 지원

## 기술 스택

### 백엔드
- **FastAPI** - 고성능 RESTful API 프레임워크
- **Python 3.x** - 메인 백엔드 언어
- **SQLAlchemy** - ORM 및 데이터베이스 관리
- **PostgreSQL** - 메인 데이터베이스 (pgvector 확장 포함)
- **Google Generative AI** - Gemini API 통합
- **Pandas** - 데이터 처리 및 분석
- **Uvicorn** - ASGI 서버

### 프론트엔드
- **Next.js 16** - React 프레임워크
- **React 19** - UI 라이브러리
- **TypeScript** - 타입 안전성
- **TailwindCSS 4** - 스타일링
- **DaisyUI** - UI 컴포넌트
- **TanStack Query** - 서버 상태 관리
- **Zustand** - 클라이언트 상태 관리
- **Chart.js** - 데이터 시각화
- **Framer Motion** - 애니메이션
- **React Hook Form + Zod** - 폼 관리 및 검증

### 인프라
- **Docker & Docker Compose** - 컨테이너화
- **Nginx** - 리버스 프록시
- **Task** - 빌드 자동화

## 설치 및 실행

### 사전 요구사항

- Docker 및 Docker Compose
- Task (선택사항, 빌드 자동화용)
- Google AI API 키 (Gemini)

### 환경 설정

1. 저장소 클론

```bash
git clone <repository-url>
cd 2025RE-ALThon-10
```

2. 환경 변수 설정

백엔드 디렉토리에 `.env` 파일 생성:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@db:5432/course_simulator
```

### Docker를 사용한 실행

#### Taskfile 사용 (권장)

```bash
# 서비스 빌드 및 시작
task start

# 서비스 중지
task stop

# 서비스 재시작
task restart
```

#### Docker Compose 직접 사용

```bash
# 빌드
docker compose -f docker/app.yml -f docker/db.yml build

# 시작
docker compose -f docker/app.yml -f docker/db.yml up -d

# 중지
docker compose -f docker/app.yml -f docker/db.yml stop
docker compose -f docker/app.yml -f docker/db.yml rm -f
```

### 로컬 개발 환경

#### 백엔드

```bash
cd backend

# 가상환경 생성
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## API 문서

### 강의 목록 조회

```http
GET /courses
```

**응답 예시:**

```json
{
  "courses": [
    {
      "id": "1",
      "course_code": "CSE2003",
      "course_name": "데이터 구조"
    }
  ]
}
```

### 강의 평가

```http
POST /courses/{course_id}/evaluate
```

**요청 본문:**

```json
{
  "taken_courses": [
    {
      "course_id": "CSE2003",
      "grade": "A"
    }
  ],
  "eval_preference": 3,
  "interests": ["AI", "Web Development"],
  "team_preference": 4,
  "attendence_type": ["online"]
}
```

**요청 필드 설명:**

- `taken_courses` (필수): 이전 수강 과목 목록
  - `course_id`: 과목 코드
  - `grade`: 취득 학점 (A, B+, 등)
- `eval_preference` (기본값: 3): 평가 선호도 (1: 시험 선호 ~ 5: 과제 선호)
- `interests` (기본값: []): 관심 분야 목록
- `team_preference` (기본값: 3): 팀 프로젝트 선호도 (1: 매우 비선호 ~ 5: 매우 선호)
- `attendence_type` (기본값: []): 선호 출석 방식 (online, offline, hybrid)

**응답 예시:**

```json
{
  "course_id": "CSE2003",
  "details": [
    {
      "criteria": "학습 적합도",
      "score": 4,
      "reason": "수강 이력: 5개 과목 이수"
    },
    {
      "criteria": "평가 방식 적합도",
      "score": 3,
      "reason": "평가 선호도 3/5"
    },
    {
      "criteria": "팀 프로젝트 적합도",
      "score": 4,
      "reason": "팀 프로젝트 선호도 4/5"
    }
  ],
  "summary": "관심 분야: AI, Web Development. 선호 출석 방식: online. 전반적으로 적합한 과목입니다."
}
```

**응답 필드 설명:**

- `course_id`: 과목 코드
- `details`: 분석 세부 정보 목록
  - `criteria`: 평가 기준명
  - `score`: 적합도 점수 (1-5)
  - `reason`: 점수 산정 근거
- `summary`: 종합 평가 요약

**오류 응답:**

- `404 Not Found`: 강의를 찾을 수 없음

## 프로젝트 구조

```
2025RE-ALThon-10/
├── backend/               # FastAPI 백엔드
│   ├── db/               # 데이터베이스 설정 및 더미 데이터
│   ├── models/           # SQLAlchemy 모델
│   ├── routers/          # API 라우터
│   ├── schemas/          # Pydantic 스키마
│   ├── scripts/          # 유틸리티 스크립트
│   └── main.py           # 애플리케이션 진입점
├── frontend/             # Next.js 프론트엔드
│   ├── src/              # 소스 코드
│   └── public/           # 정적 파일
├── docker/               # Docker 설정 파일
├── nginx/                # Nginx 설정
├── Taskfile.yml          # Task 빌드 자동화
└── README.md             # 프로젝트 문서
```

## 데이터베이스 초기화

강의 데이터를 Excel 파일에서 임포트하려면:

```bash
# 백엔드 컨테이너 내에서 실행
python backend/scripts/import_courses.py
```

## 개발 가이드

### 새로운 API 엔드포인트 추가

1. `backend/routers/`에 새 라우터 생성
2. `backend/schemas/`에 요청/응답 스키마 정의
3. 필요시 `backend/models/`에 데이터베이스 모델 추가
4. `backend/main.py`에 라우터 등록

### 프론트엔드 페이지 추가

1. `frontend/src/app/`에 새 라우트 디렉토리 생성
2. `page.tsx` 파일로 페이지 컴포넌트 정의
3. 필요시 공통 컴포넌트를 `frontend/src/components/`에 추가

## 라이선스

이 프로젝트는 2025 RE-ALThon 해커톤을 위해 개발되었습니다.