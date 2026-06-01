# ai-pick


Claude Code 릴리스마다 '지금 써볼 만한 변화'를 골라주는 changelog 큐레이션.

🔗 **라이브 데모 · 케이스 스터디** → https://tech.sungd.uk/projects/claude-code-tracking

## 이렇게 쓴다

1. 릴리스별 분류(기능·수정·실험)로 훑는다
2. Pick에서 당장 써볼 것만 본다
3. 카테고리 뷰로 주제별로 모아본다

Claude Code changelog 큐레이션 — 매 릴리스에서 "오늘 써볼 만한 것"을 골라준다.

**Live**: [ai.sungd.uk](https://ai.sungd.uk)

## 뭐가 다른가

[공식 changelog](https://code.claude.com/docs/en/changelog)는 시간순 raw 목록. 빠짐없지만 매주 릴리스가 1~2개씩 쏟아져 어떤 게 정말 써볼 만한지 가려내기 어렵다.

이 페이지는 같은 데이터를 **3가지 시각**으로 재구성한다:

1. **🎯 오늘 써볼 기능** — 최근 릴리스에서 직접 써볼 만한 기능 6개. 각각 "왜 효과적인지" + "써보면서 학습할 포인트" 표시
2. **🧰 용도별로 보기** — 8개 카테고리(긴 작업·멀티 세션·PR·비용·UI·플러그인·Hook·Enterprise)로 묶어 "이럴 때 뭐 썼더라" 떠올리기
3. **버전별 changelog** — Feature는 한 줄 노출, 개선/보안/수정은 탭으로 접어 컴팩트하게

추가:
- 며칠 전 배지 히트맵 (빨강 → 주황 → 노랑 → 흐림)
- 명령어 클릭 → 공식 docs 정확한 섹션으로 deep link (Text Fragment)
- 버전 배지 클릭 → 공식 changelog 페이지의 해당 버전 앵커
- 라이트 / 다크 모드 토글 (기본 라이트)

## 업데이트 자동화

매일 06:30(KST) GitHub Actions가 자동 실행 (`.github/workflows/daily-update.yml`):

1. **버전 목록** (`scripts/update_changelog.py`, 토큰 0) — CHANGELOG.md fetch → 새 버전 감지 → 분류(feature/improve/security/fix) → HTML 블록 생성·삽입 → 커밋
2. **Pick·용도별 큐레이션** (새 feature 있을 때만) — Claude Code Action이 판단해서 🎯 Pick·🧰 카테고리 갱신

대부분의 날은 1단계(무료)만 돌고, 주목할 새 기능이 나온 날만 Claude가 판단 작업을 한다.

### 셋업 (1회)

1. [Claude GitHub App](https://github.com/apps/claude)을 이 repo에 설치
2. 터미널에서 `claude setup-token` (Pro/Max 구독) → OAuth 토큰 발급
3. repo Settings → Secrets → `CLAUDE_CODE_OAUTH_TOKEN` 등록

> API 키 대신 구독 토큰 사용 → 별도 과금 없음.

## 기술 스택

- 단일 정적 HTML, 빌드 없음
- Pretendard Variable (본문) + Google Sans Code (모노)
- GitHub Pages

## 라이선스

MIT
