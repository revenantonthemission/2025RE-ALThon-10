from typing import List
from core.schema import UserProfile, CourseHistory

# --- 엄청 긴 데이터 리스트 ---
FULL_DUMMY_DATA: List[UserProfile] = [

# 시연 페르소나:
# UserProfile(
#    taken_courses=[
#        CourseHistory(course_id="파이썬프로그래밍", grade="A+"),
#        CourseHistory(course_id="선형대수학", grade="A")
#    ],
#    eval_preference=5,  # 과제/프로젝트 선호 (5점)
#    interests=["인공지능", "딥러닝", "파이토치"],
#    team_preference=1,  # 팀플 매우 싫음 (1점) -> 핵심 매칭 포인트
#    attendence_type=["오프라인"]
#   )

        # [타겟 그룹 AT] 시연용 정답 데이터 1 (AI + 팀플극혐 + 딥러닝실습 수강)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="파이썬프로그래밍", grade="A+"),
                CourseHistory(course_id="인공지능개론", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A+"), # <--- 정답 강의
                CourseHistory(course_id="확률과통계", grade="B+")
            ],
            eval_preference=5,  # 과제 선호
            interests=["인공지능", "딥러닝", "Keras"],
            team_preference=1,  # 팀플 싫음 (페르소나와 일치)
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 AU] 시연용 정답 데이터 2
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="선형대수학", grade="A"),
                CourseHistory(course_id="기계학습", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A"), # <--- 정답 강의
                CourseHistory(course_id="컴퓨터비전", grade="B+")
            ],
            eval_preference=5,
            interests=["머신러닝", "Pytorch", "AI"],
            team_preference=1,  # 독고다이 성향
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 AV] 시연용 정답 데이터 3
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="데이터과학", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A+"), # <--- 정답 강의
                CourseHistory(course_id="자연어처리", grade="A"),
                CourseHistory(course_id="파이썬응용", grade="B")
            ],
            eval_preference=4,
            interests=["데이터분석", "딥러닝", "Tensorflow"],
            team_preference=1,  # 조별과제 스트레스 싫음
            attendence_type=["오프라인", "전자출석"]
        ),

        # [타겟 그룹 AW] 시연용 정답 데이터 4
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="딥러닝실습", grade="A"), # <--- 정답 강의
                CourseHistory(course_id="강화학습", grade="B+"),
                CourseHistory(course_id="알고리즘", grade="A"),
                CourseHistory(course_id="자료구조", grade="B+")
            ],
            eval_preference=5,
            interests=["AI", "ReinforcementLearning", "로봇"],
            team_preference=1,  # 혼자 연구하는 것 선호
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 AX] 시연용 정답 데이터 5
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="인공지능수학", grade="B+"),
                CourseHistory(course_id="패턴인식", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A"), # <--- 정답 강의
                CourseHistory(course_id="영상처리", grade="A")
            ],
            eval_preference=5,
            interests=["CV", "Vision", "딥러닝"],
            team_preference=1,  # 팀원 설득하는 과정 귀찮음
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 AY] 시연용 정답 데이터 6
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="빅데이터분석", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="B+"), # <--- 정답 강의
                CourseHistory(course_id="클라우드컴퓨팅", grade="B"),
                CourseHistory(course_id="파이썬기초", grade="A+")
            ],
            eval_preference=4,
            interests=["BigData", "AI", "데이터엔지니어링"],
            team_preference=1,  # 내 속도대로 프로젝트 진행 원함
            attendence_type=["온라인"]
        ),

        # [타겟 그룹 AZ] 시연용 정답 데이터 7
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="통계적학습", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A+"), # <--- 정답 강의
                CourseHistory(course_id="R프로그래밍", grade="B+"),
                CourseHistory(course_id="데이터마이닝", grade="A")
            ],
            eval_preference=5,
            interests=["통계", "딥러닝", "분석"],
            team_preference=2,  # 팀플 별로 안 좋아함
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 BA] 시연용 정답 데이터 8
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="고급인공지능", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A"), # <--- 정답 강의
                CourseHistory(course_id="자율주행개론", grade="B"),
                CourseHistory(course_id="C++프로그래밍", grade="B+")
            ],
            eval_preference=5,
            interests=["Autonomous", "AI", "DeepLearning"],
            team_preference=1,  # 책임 소재 명확한 개인 과제 선호
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 BB] 시연용 정답 데이터 9
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="음성인식", grade="A"),
                CourseHistory(course_id="신호처리", grade="B+"),
                CourseHistory(course_id="딥러닝실습", grade="A+"), # <--- 정답 강의
                CourseHistory(course_id="매트랩", grade="B")
            ],
            eval_preference=5,
            interests=["Audio", "Speech", "AI"],
            team_preference=1,  # 예술가적 기질, 혼자 작업
            attendence_type=["오프라인"]
        ),

        # [타겟 그룹 BC] 시연용 정답 데이터 10
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="생성형AI", grade="A+"),
                CourseHistory(course_id="NLP", grade="A"),
                CourseHistory(course_id="딥러닝실습", grade="A"), # <--- 정답 강의
                CourseHistory(course_id="프롬프트엔지니어링", grade="A")
            ],
            eval_preference=5,
            interests=["GenAI", "LLM", "GPT"],
            team_preference=1,  # 최신 기술 혼자 파는 것 좋아함
            attendence_type=["온라인", "전자출석"]
        ),

        # [유형 A] AI/데이터 덕후 (과제 선호, 팀플 싫음, 오프라인)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="파이썬프로그래밍", grade="A+"),
                CourseHistory(course_id="선형대수학", grade="B+"),
                CourseHistory(course_id="데이터구조", grade="A"),
                CourseHistory(course_id="확률과통계", grade="A")
            ],
            eval_preference=5,  # 과제/프로젝트 파
            interests=["인공지능", "데이터사이언스", "머신러닝"],
            team_preference=1,  # 팀플 극혐 (혼자 하는 게 편함)
            attendence_type=["오프라인", "전자출석"]
        ),

        # [유형 B] 전통적인 CS 공학도 (시험 선호, 시스템/보안, 팀플 보통)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="C프로그래밍", grade="B+"),
                CourseHistory(course_id="컴퓨터구조", grade="A"),
                CourseHistory(course_id="운영체제", grade="B"),
                CourseHistory(course_id="이산수학", grade="A")
            ],
            eval_preference=1,  # 시험 파 (깔끔하게 끝내는 거 선호)
            interests=["시스템", "보안", "네트워크"],
            team_preference=3,  # 팀플 있으면 하고 없으면 말고
            attendence_type=["오프라인"]
        ),

        # [유형 C] 웹/앱 개발자 (프로젝트 선호, 팀플 매우 좋음, 온라인 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="웹프로그래밍기초", grade="A+"),
                CourseHistory(course_id="자바프로그래밍", grade="A"),
                CourseHistory(course_id="데이터베이스", grade="B+"),
                CourseHistory(course_id="컴퓨터네트워크", grade="B")
            ],
            eval_preference=4,  # 프로젝트 선호
            interests=["웹개발", "프론트엔드", "백엔드"],
            team_preference=5,  # 팀플 리더 스타일
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 D] 융합형 인재 (팀플 좋음, 기획/설계, 출석 상관없음)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="창의적공학설계", grade="A+"),
                CourseHistory(course_id="기술경영", grade="A"),
                CourseHistory(course_id="소프트웨어공학", grade="A"),
                CourseHistory(course_id="HCI", grade="A")
            ],
            eval_preference=3,  # 반반
            interests=["기획", "UI/UX", "PM"],
            team_preference=5,  # 협업 매우 선호
            attendence_type=["온라인", "오프라인"]
        ),

        # [유형 E] 벼락치기형 (시험 선호, 팀플 싫음, 온라인 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="교양영어", grade="C+"),
                CourseHistory(course_id="컴퓨터개론", grade="B"),
                CourseHistory(course_id="오픈소스소프트웨어", grade="B+")
            ],
            eval_preference=2,  # 시험 선호 (과제 귀찮음)
            interests=["게임개발", "그래픽스"],
            team_preference=2,  # 팀플 별로
            attendence_type=["온라인", "전자출석"]
        ),
        # [유형 F] 수학/이론 덕후 (코딩보다는 증명 선호, 시험 선호, 팀플 보통)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="미적분학II", grade="A+"),
                CourseHistory(course_id="이산수학", grade="A"),
                CourseHistory(course_id="알고리즘", grade="A+"),
                CourseHistory(course_id="오토마타및형식언어", grade="A")
            ],
            eval_preference=1,  # 시험 선호 (명확한 정답이 있는 것을 좋아함)
            interests=["알고리즘", "수학", "계산이론"],
            team_preference=3,  # 크게 상관없음
            attendence_type=["오프라인"]
        ),

        # [유형 G] 임베디드/IoT 개발자 (하드웨어 제어, 실습 선호, 팀플 좋음)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="논리회로", grade="B+"),
                CourseHistory(course_id="C프로그래밍", grade="A"),
                CourseHistory(course_id="마이크로프로세서", grade="B+"),
                CourseHistory(course_id="임베디드시스템", grade="A")
            ],
            eval_preference=4,  # 실습/프로젝트 선호
            interests=["IoT", "로보틱스", "임베디드", "아두이노"],
            team_preference=4,  # 하드웨어는 팀 작업이 많아 선호
            attendence_type=["오프라인"]  # 장비 때문에 오프라인 필수
        ),

        # [유형 H] 게임 개발 지망생 (그래픽스/엔진, 프로젝트 선호, 밤샘 코딩 가능)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="C++프로그래밍", grade="A"),
                CourseHistory(course_id="컴퓨터그래픽스", grade="A+"),
                CourseHistory(course_id="선형대수학", grade="C+"), # 수학은 좀 어려워함
                CourseHistory(course_id="객체지향프로그래밍", grade="B+")
            ],
            eval_preference=5,  # 결과물(게임) 만드는 과제 선호
            interests=["게임개발", "유니티", "언리얼", "VR/AR"],
            team_preference=4,  # 게임 잼 등 팀 협업 익숙
            attendence_type=["온라인", "전자출석"]
        ),

        # [유형 I] 정보보안/화이트해커 (실습 위주, 독자적 성향, 이론 시험 싫음)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="컴퓨터네트워크", grade="A"),
                CourseHistory(course_id="운영체제", grade="B+"),
                CourseHistory(course_id="암호학", grade="B"),
                CourseHistory(course_id="리눅스시스템", grade="A")
            ],
            eval_preference=4,  # CTF나 실습 과제 선호
            interests=["해킹", "정보보안", "네트워크보안"],
            team_preference=2,  # 혼자 파고드는 성향 강함
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 J] 클라우드/DevOps 엔지니어 (최신 기술 선호, 프로젝트 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="리눅스기초", grade="A"),
                CourseHistory(course_id="데이터베이스", grade="A"),
                CourseHistory(course_id="웹서비스설계", grade="B+"),
                CourseHistory(course_id="분산시스템", grade="B")
            ],
            eval_preference=5,  # 구축 프로젝트 선호
            interests=["클라우드", "AWS", "Docker", "DevOps"],
            team_preference=4,  # 협업 툴(Git 등) 사용 익숙
            attendence_type=["온라인"]
        ),

        # [유형 K] 금융/핀테크 관심 (통계 중시, 시험 선호, 꼼꼼함)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="경영학원론", grade="A"),
                CourseHistory(course_id="확률과통계", grade="A+"),
                CourseHistory(course_id="파이썬프로그래밍", grade="B"),
                CourseHistory(course_id="블록체인개론", grade="B+")
            ],
            eval_preference=2,  # 시험 위주 평가 선호
            interests=["핀테크", "블록체인", "금융IT", "데이터분석"],
            team_preference=3,  # 보통
            attendence_type=["오프라인"]
        ),

        # [유형 L] 복수전공/전과생 (기초 과목 위주, 열심히 함, 팀플 부담스러움)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="컴퓨터적사고", grade="A+"),
                CourseHistory(course_id="파이썬기초", grade="A"),
                CourseHistory(course_id="웹코딩입문", grade="A"),
                CourseHistory(course_id="인문학의이해", grade="A")
            ],
            eval_preference=3,  # 아직 잘 몰라서 반반
            interests=["기초코딩", "웹사이트", "IT교양"],
            team_preference=2,  # 민폐 끼칠까 봐 팀플 기피
            attendence_type=["오프라인", "전자출석"]
        ),

        # [유형 M] 대학원 진학 희망 (학점 관리 철저, 이론/연구 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="인공지능", grade="A+"),
                CourseHistory(course_id="알고리즘", grade="A+"),
                CourseHistory(course_id="자연어처리", grade="A"),
                CourseHistory(course_id="컴퓨터비전", grade="A")
            ],
            eval_preference=2,  # 논문 리뷰나 시험 선호
            interests=["NLP", "CV", "연구", "논문"],
            team_preference=1,  # 성적 리스크 때문에 팀플 싫음
            attendence_type=["오프라인"]  # 교수님 눈도장
        ),

        # [유형 N] 창업/기획 지망 (개발은 적당히, 네트워킹/팀플 매우 중요)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="스타트업기초", grade="A"),
                CourseHistory(course_id="웹프로그래밍", grade="B"),
                CourseHistory(course_id="모바일앱개발", grade="B-"),
                CourseHistory(course_id="IT비즈니스", grade="A+")
            ],
            eval_preference=5,  # 아이디어 피칭, 프로젝트 선호
            interests=["창업", "서비스기획", "앱서비스"],
            team_preference=5,  # 사람 만나는 것 좋아함
            attendence_type=["오프라인"]
        ),

        # [유형 O] "F만 면하자" (최소한의 노력, 쉬운 과목 선호, 팀플 묻어가기)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="영화의이해", grade="B+"),
                CourseHistory(course_id="생활속의컴퓨터", grade="B"),
                CourseHistory(course_id="C프로그래밍", grade="C+"),
                CourseHistory(course_id="글쓰기", grade="B")
            ],
            eval_preference=3,  # 뭐든 쉬운 거 선호
            interests=["교양", "꿀강", "학점방어"],
            team_preference=4,  # 버스 타기 위해 팀플 선호
            attendence_type=["온라인", "녹화강의"]  # 학교 가기 싫음
        ),
        # [유형 P] 알고리즘 대회(PS) 매니아 (명확한 정답 선호, 주관적 평가 싫음)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="자료구조", grade="A+"),
                CourseHistory(course_id="알고리즘", grade="A+"),
                CourseHistory(course_id="고급알고리즘", grade="A"),
                CourseHistory(course_id="C++프로그래밍", grade="A")
            ],
            eval_preference=1,  # 코딩 테스트처럼 정답이 딱 떨어지는 시험 선호
            interests=["알고리즘", "코딩테스트", "백준", "PS"],
            team_preference=2,  # 내 실력대로 평가받고 싶음
            attendence_type=["온라인"]  # 강의보다 혼자 문제 푸는 게 효율적
        ),

        # [유형 Q] 프론트엔드/UI 개발 (디자인 감각 중요, 눈에 보이는 결과물 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="웹프로그래밍", grade="A"),
                CourseHistory(course_id="HCI개론", grade="A"),
                CourseHistory(course_id="모바일앱디자인", grade="B+"),
                CourseHistory(course_id="자바스크립트심화", grade="A")
            ],
            eval_preference=5,  # 포트폴리오용 프로젝트 선호
            interests=["React", "Vue", "CSS", "UI디자인"],
            team_preference=4,  # 디자이너/기획자와 협업 즐김
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 R] 데이터 분석가 지망 (통계/SQL 중시, 비즈니스 인사이트)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="통계학개론", grade="A"),
                CourseHistory(course_id="데이터베이스", grade="A"),
                CourseHistory(course_id="경영정보시스템", grade="B+"),
                CourseHistory(course_id="데이터시각화", grade="A")
            ],
            eval_preference=4,  # 분석 리포트 과제 선호
            interests=["SQL", "Tableau", "데이터분석", "비즈니스"],
            team_preference=3,  # 무난함
            attendence_type=["오프라인"]
        ),

        # [유형 S] 백엔드/서버 엔지니어 (대용량 트래픽, 아키텍처 관심, 묵직한 과목 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="운영체제", grade="B+"),
                CourseHistory(course_id="네트워크프로그래밍", grade="A"),
                CourseHistory(course_id="데이터베이스시스템", grade="A"),
                CourseHistory(course_id="분산처리", grade="B+")
            ],
            eval_preference=3,  # 이론과 실습의 조화 중요
            interests=["Spring", "Java", "서버", "아키텍처"],
            team_preference=4,  # API 연동 등 협업 필수라 생각
            attendence_type=["오프라인", "전자출석"]
        ),

        # [유형 T] 모바일 앱 개발자 (Android/iOS, 개인 프로젝트 다수)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="자바프로그래밍", grade="B+"),
                CourseHistory(course_id="객체지향설계", grade="A"),
                CourseHistory(course_id="모바일프로그래밍", grade="A+"),
                CourseHistory(course_id="스마트폰앱실습", grade="A")
            ],
            eval_preference=5,  # 앱 출시 과제 선호
            interests=["안드로이드", "iOS", "플러터", "앱개발"],
            team_preference=2,  # 혼자서도 앱 하나 뚝딱 만듦
            attendence_type=["온라인"]
        ),

        # [유형 U] 자율주행/로보틱스 (하드웨어+AI 융합, 수학 필수)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="선형대수학", grade="B"),
                CourseHistory(course_id="컴퓨터비전", grade="B+"),
                CourseHistory(course_id="제어공학", grade="A"),
                CourseHistory(course_id="임베디드소프트웨어", grade="A")
            ],
            eval_preference=4,  # 실제 로봇 구동 실습 선호
            interests=["자율주행", "ROS", "SLAM", "로봇"],
            team_preference=5,  # 하드웨어 세팅 등 혼자 불가능
            attendence_type=["오프라인"]  # 실습실 출근 도장
        ),

        # [유형 V] 인문학 융합형 (비전공 베이스, 코딩 어려워함, 인문/사회 데이터 관심)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="파이썬기초", grade="A"),
                CourseHistory(course_id="디지털인문학", grade="A+"),
                CourseHistory(course_id="텍스트마이닝", grade="B"),
                CourseHistory(course_id="사회연결망분석", grade="B+")
            ],
            eval_preference=5,  # 에세이나 보고서 형태 과제 선호
            interests=["빅데이터", "인문학", "사회학", "시각화"],
            team_preference=3,  # 소통 능력 좋음
            attendence_type=["오프라인"]
        ),

        # [유형 W] QA/테스팅 엔지니어 (꼼꼼함, 버그 찾기, 안정성 중시)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="소프트웨어공학", grade="A"),
                CourseHistory(course_id="웹프로그래밍", grade="B"),
                CourseHistory(course_id="시스템분석설계", grade="A"),
                CourseHistory(course_id="자바프로그래밍", grade="B+")
            ],
            eval_preference=3,  # 명세서 작성 등 문서화 과제 선호
            interests=["QA", "테스팅", "유지보수", "클린코드"],
            team_preference=4,  # 팀의 품질 관리자 역할
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 X] 해외 취업 목표 (영어 강의 선호, 글로벌 트렌드)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="TechnicalWriting", grade="A"),
                CourseHistory(course_id="GlobalCapstone", grade="A"),
                CourseHistory(course_id="알고리즘(영어강의)", grade="B+"),
                CourseHistory(course_id="실리콘밸리문화", grade="P")
            ],
            eval_preference=5,  # 영어 프레젠테이션 선호
            interests=["해외취업", "영어", "링크드인", "글로벌"],
            team_preference=5,  # 외국인 교환학생과 팀플 선호
            attendence_type=["오프라인"]
        ),

        # [유형 Y] VR/AR 메타버스 관심 (그래픽스+콘텐츠, 게임과 유사하지만 다름)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="컴퓨터그래픽스", grade="B"),
                CourseHistory(course_id="가상현실개론", grade="A"),
                CourseHistory(course_id="인터랙티브미디어", grade="A+"),
                CourseHistory(course_id="C#프로그래밍", grade="A")
            ],
            eval_preference=5,  # 시연 가능한 콘텐츠 제작 선호
            interests=["VR", "AR", "메타버스", "유니티"],
            team_preference=4,  # 콘텐츠 기획자와 개발자 협업
            attendence_type=["오프라인", "전자출석"]
        ),
        # [유형 Z] 블록체인/Web3 개발자 (탈중앙화, 스마트 컨트랙트, 신기술 덕후)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="암호학", grade="A"),
                CourseHistory(course_id="분산시스템", grade="B+"),
                CourseHistory(course_id="네트워크프로그래밍", grade="A"),
                CourseHistory(course_id="핀테크개론", grade="A")
            ],
            eval_preference=5,  # DApp 개발 프로젝트 선호
            interests=["블록체인", "이더리움", "Solidity", "NFT"],
            team_preference=3,  # 오픈소스 커뮤니티 스타일 협업
            attendence_type=["온라인"]
        ),

        # [유형 AA] 반도체/FPGA 하드웨어 설계 (Low-level, 논리회로, 칼퇴 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="디지털논리회로", grade="A+"),
                CourseHistory(course_id="컴퓨터구조", grade="A"),
                CourseHistory(course_id="VHDL설계", grade="A"),
                CourseHistory(course_id="집적회로", grade="B+")
            ],
            eval_preference=2,  # 정확한 타이밍과 동작 검증(시험/실습) 중시
            interests=["Verilog", "FPGA", "ASIC", "반도체"],
            team_preference=2,  # 하드웨어 디버깅은 혼자가 편함
            attendence_type=["오프라인"]  # 장비 사용 필수
        ),

        # [유형 AB] 데이터 엔지니어 (분석보다는 파이프라인 구축, 대용량 처리)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="데이터베이스시스템", grade="A"),
                CourseHistory(course_id="빅데이터처리", grade="A+"),
                CourseHistory(course_id="클라우드컴퓨팅", grade="B+"),
                CourseHistory(course_id="자료구조", grade="B")
            ],
            eval_preference=4,  # 시스템 구축 과제 선호
            interests=["ETL", "Hadoop", "Spark", "Kafka"],
            team_preference=4,  # 데이터 사이언티스트와 협업
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 AC] 컴퓨터교육/에듀테크 (가르치는 것 좋아함, 설명 잘함)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="컴퓨터교육론", grade="A+"),
                CourseHistory(course_id="스크래치코딩", grade="A+"),
                CourseHistory(course_id="웹프로그래밍", grade="A"),
                CourseHistory(course_id="교육심리학", grade="A")
            ],
            eval_preference=5,  # 교안 만들기, 발표 과제 선호
            interests=["교육", "멘토링", "알고리즘교육", "교직"],
            team_preference=5,  # 스터디장, 조장 전문
            attendence_type=["오프라인"]  # 상호작용 중시
        ),

        # [유형 AD] 오디오/멀티미디어 처리 (신호처리, 음악, 예술 융합)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="신호및시스템", grade="B"),
                CourseHistory(course_id="디지털신호처리", grade="A"),
                CourseHistory(course_id="멀티미디어개론", grade="A"),
                CourseHistory(course_id="Python응용", grade="B+")
            ],
            eval_preference=5,  # 오디오 필터 만들기 등 창작 과제
            interests=["DSP", "음성인식", "미디어아트", "Sound"],
            team_preference=3,  # 예술적 취향 맞으면 좋음
            attendence_type=["오프라인", "전자출석"]
        ),

        # [유형 AE] 컴파일러/언어론 덕후 (원리 파악 중시, 난해한 과목 선호)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="오토마타", grade="A+"),
                CourseHistory(course_id="컴파일러구성", grade="A+"),
                CourseHistory(course_id="프로그래밍언어론", grade="A"),
                CourseHistory(course_id="시스템프로그래밍", grade="A")
            ],
            eval_preference=1,  # 이론 시험 끝판왕 선호
            interests=["LLVM", "Rust", "파싱", "언어설계"],
            team_preference=1,  # 대화가 통하는 사람이 드물어 혼자 함
            attendence_type=["오프라인"]
        ),

        # [유형 AF] 고성능 컴퓨팅(HPC) (최적화, 병렬처리, 속도에 집착)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="병렬컴퓨팅", grade="A"),
                CourseHistory(course_id="GPU프로그래밍", grade="A+"),
                CourseHistory(course_id="C++심화", grade="A"),
                CourseHistory(course_id="운영체제", grade="B+")
            ],
            eval_preference=3,  # 성능 최적화 과제 선호
            interests=["CUDA", "MPI", "Supercomputer", "최적화"],
            team_preference=2,  # 코드 스타일 다르면 스트레스 받음
            attendence_type=["온라인"]
        ),

        # [유형 AG] UI/UX 리서처 (코딩보다는 사용자 경험 분석, 심리학)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="HCI", grade="A+"),
                CourseHistory(course_id="인지심리학", grade="A"),
                CourseHistory(course_id="통계학", grade="B"),
                CourseHistory(course_id="웹디자인", grade="A")
            ],
            eval_preference=5,  # 사용자 설문조사, 분석 보고서 선호
            interests=["UX리서치", "사용자경험", "Usability", "디자인"],
            team_preference=5,  # 사람 관찰하고 인터뷰하는 것 좋아함
            attendence_type=["오프라인"]
        ),

        # [유형 AH] 금융공학/퀀트 (수학+개발+금융, 고수익 목표)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="금융공학", grade="A"),
                CourseHistory(course_id="수치해석", grade="A"),
                CourseHistory(course_id="알고리즘트레이딩", grade="A+"),
                CourseHistory(course_id="파이썬데이터분석", grade="A")
            ],
            eval_preference=2,  # 모델링 결과 및 수익률 검증 선호
            interests=["주식", "퀀트", "알고리즘매매", "금융"],
            team_preference=2,  # 전략 노출 꺼림, 독자 행동
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 AI] 네트워크 엔지니어 (인프라, 라우팅, 하드웨어 세팅)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="데이터통신", grade="B+"),
                CourseHistory(course_id="컴퓨터네트워크", grade="A"),
                CourseHistory(course_id="TCP/IP프로토콜", grade="A"),
                CourseHistory(course_id="네트워크실습", grade="A+")
            ],
            eval_preference=4,  # 패킷 트레이서 등 실습 선호
            interests=["Cisco", "네트워크관리", "서버실", "5G"],
            team_preference=4,  # 망 구축은 팀 단위 작업
            attendence_type=["오프라인"]  # 실습 장비 필요
        ),
        # [유형 AJ] 바이오인포매틱스 (생물학+컴공 융합, 연구실 성향)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="일반생물학", grade="A"),
                CourseHistory(course_id="파이썬프로그래밍", grade="A"),
                CourseHistory(course_id="생물정보학개론", grade="A+"),
                CourseHistory(course_id="데이터마이닝", grade="B+")
            ],
            eval_preference=3,  # 실험 보고서나 데이터 분석 과제 선호
            interests=["DNA", "유전체", "바이오", "신약개발"],
            team_preference=2,  # 연구 데이터 분석은 혼자 집중
            attendence_type=["오프라인"]  # 랩실 생활 익숙
        ),

        # [유형 AK] GIS/지도 서비스 개발 (지리정보, 위치기반서비스, 시각화)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="데이터베이스", grade="B+"),
                CourseHistory(course_id="GIS개론", grade="A"),
                CourseHistory(course_id="공간데이터분석", grade="A+"),
                CourseHistory(course_id="웹프로그래밍", grade="B")
            ],
            eval_preference=4,  # 지도 API 연동 프로젝트 선호
            interests=["지도", "LBS", "내비게이션", "공간정보"],
            team_preference=3,  # 무난함
            attendence_type=["온라인", "전자출석"]
        ),

        # [유형 AL] 기술 영업/IT 컨설턴트 (코딩 깊이보다는 넓은 지식, 발표 왕)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="경영정보시스템", grade="A+"),
                CourseHistory(course_id="IT트렌드분석", grade="A"),
                CourseHistory(course_id="소프트웨어공학", grade="B"),
                CourseHistory(course_id="웹개론", grade="B+")
            ],
            eval_preference=5,  # 발표, 제안서 작성, 피칭 선호
            interests=["IT영업", "컨설팅", "솔루션", "커뮤니케이션"],
            team_preference=5,  # 사람 만나는 게 일
            attendence_type=["오프라인"]
        ),

        # [유형 AM] 시스템 관리자/SRE (리눅스 덕후, 쉘 스크립트, 안정성 중시)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="리눅스시스템", grade="A+"),
                CourseHistory(course_id="스크립트언어", grade="A"),
                CourseHistory(course_id="서버구축실습", grade="A"),
                CourseHistory(course_id="네트워크보안", grade="B")
            ],
            eval_preference=4,  # 서버 구축 및 트러블슈팅 과제 선호
            interests=["Linux", "Shell", "서버관리", "엔지니어링"],
            team_preference=2,  # 터미널과 대화하는 게 편함
            attendence_type=["온라인"]
        ),

        # [유형 AN] 양자 컴퓨팅 연구 (물리학 베이스, 극도의 난이도 즐김)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="양자역학개론", grade="A"),
                CourseHistory(course_id="선형대수학", grade="A+"),
                CourseHistory(course_id="양자컴퓨팅", grade="A+"),
                CourseHistory(course_id="고급알고리즘", grade="A")
            ],
            eval_preference=1,  # 수식 증명 및 이론 시험 선호
            interests=["Quantum", "Qiskit", "물리학", "미래기술"],
            team_preference=1,  # 이해하는 사람이 없어 혼자 공부
            attendence_type=["오프라인"]
        ),

        # [유형 AO] 웹 접근성/표준 전문가 (윤리적 코딩, HTML/CSS 장인)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="웹표준기술", grade="A+"),
                CourseHistory(course_id="인터넷윤리", grade="A"),
                CourseHistory(course_id="HCI", grade="A"),
                CourseHistory(course_id="프론트엔드기초", grade="A")
            ],
            eval_preference=3,  # 마크업 검증 등 꼼꼼한 과제
            interests=["접근성", "A11y", "웹표준", "약자배려"],
            team_preference=5,  # 모두를 위한 서비스를 만드는데 협력 중요
            attendence_type=["온라인", "녹화강의"]
        ),

        # [유형 AP] 리걸테크/지식재산권 (법학 부전공, 논리적, 문서화)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="지식재산권개론", grade="A"),
                CourseHistory(course_id="생활과법률", grade="A"),
                CourseHistory(course_id="데이터베이스", grade="B"),
                CourseHistory(course_id="정보보호법규", grade="A+")
            ],
            eval_preference=2,  # 판례 분석, 레포트, 시험 선호
            interests=["특허", "저작권", "소프트웨어법", "컴플라이언스"],
            team_preference=3,  # 토론 좋아함
            attendence_type=["오프라인"]
        ),

        # [유형 AQ] 전산언어학/NLP (언어학 관심, 텍스트 처리)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="언어학개론", grade="A"),
                CourseHistory(course_id="자연어처리", grade="B+"),
                CourseHistory(course_id="파이썬프로그래밍", grade="A"),
                CourseHistory(course_id="형식언어", grade="B+")
            ],
            eval_preference=3,  # 텍스트 분석 리포트
            interests=["형태소분석", "언어모델", "번역", "인문학융합"],
            team_preference=2,  # 조용히 텍스트 파는 것 좋아함
            attendence_type=["온라인"]
        ),

        # [유형 AR] 데이터 시각화 아티스트 (디자인+코드, D3.js, 예술적 감각)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="웹프로그래밍", grade="A"),
                CourseHistory(course_id="디자인기초", grade="A"),
                CourseHistory(course_id="데이터시각화", grade="A+"),
                CourseHistory(course_id="컴퓨터그래픽스", grade="B")
            ],
            eval_preference=5,  # 시각적으로 화려한 결과물 선호
            interests=["D3.js", "Processing", "미디어아트", "시각화"],
            team_preference=4,  # 전시회 준비하듯 협업
            attendence_type=["오프라인", "전자출석"]
        ),

        # [유형 AS] 스마트시티/IoT 도시계획 (거시적 관점, 센서 데이터)
        UserProfile(
            taken_courses=[
                CourseHistory(course_id="도시계획론", grade="B+"),
                CourseHistory(course_id="IoT시스템", grade="A"),
                CourseHistory(course_id="빅데이터개론", grade="B+"),
                CourseHistory(course_id="네트워크프로그래밍", grade="B")
            ],
            eval_preference=5,  # 도시 문제 해결 프로젝트 선호
            interests=["스마트시티", "환경", "공공데이터", "센서"],
            team_preference=5,  # 다양한 전공생과 팀플 즐김
            attendence_type=["오프라인"]
        )
    ]