# ai-pick

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

## 업데이트 주기

매 Claude Code 릴리스 후 수동 갱신. Claude Code 자체 스킬로 반자동화 — CHANGELOG.md fetch → 분류 → HTML 삽입.

## 기술 스택

- 단일 정적 HTML, 빌드 없음
- Pretendard Variable (본문) + Google Sans Code (모노)
- GitHub Pages

## 라이선스

MIT
