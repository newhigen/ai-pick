# HISTORY

ai-pick (Agent Edge) 변천사. 최신이 맨 위.

## 2026-06-10 — 자동화 전 탭 확대 (Codex·Manus·뉴스) + stage-2 수리

- **무엇**: 그동안 Claude Code 한 탭만 자동 갱신되고 Codex·Manus·뉴스는 ~2-3주 방치였음. ① stage-2 큐레이션이 `claude-code-action@v1`(PR 모드라 워킹트리 미편집)으로 **한 번도 커밋 안 되던 버그를 헤드리스 `claude -p`로 교체**해 수리. ② `update_codex.py` 신규 — openai/codex GitHub Releases(stable만)로 Codex 버전 블록 자동 삽입. ③ `collect_blog.py`에 anthropic.com/news·openai.com 추가. ④ `curate_prompt.md`를 CC·Codex·Manus·뉴스 4탭 커버로 확장.
- **왜**: "Claude Code만 잘 되고 나머지는 죽어있다"는 문제. 큐레이션 파이프라인이 PR 모드 액션이라 워킹트리를 안 고쳐 매번 noop(이력상 큐레이션 커밋 0건)이었고, Codex/Manus/뉴스는 수집 소스 자체가 없었음.
- **핵심 결정·교훈**: Codex는 changelog형이라 **결정적 스크립트**로 버전 블록 생성(LLM 불필요), 써볼·Manus·뉴스 배치만 stage-2 LLM이 "기존 항목 복사→값 교체" 전략으로. 모델 출시 발표(Fable 5)를 컷오프 이후라 "가짜"로 오판했던 사고 → **추측 금지, WebSearch 검증** 룰을 프롬프트에 못박음.

## 2026-05-30 — Agent Edge 리브랜딩 + 5탭 IA 개편

- **무엇**: 단일 Claude Code 중심에서 **5탭 IA(홈·Claude Code·Codex·Manus·뉴스)**로 확장. 이름을 **Agent Edge**로 확정하고 마크를 `>_` 터미널 프롬프트(`>`=전진/edge), 액센트를 보라(`--pick #6b4cff`)로 통일. blog·Manus 항목에 분석 모달(효과성·원리·맥락) + 개념 다이어그램(병렬·양방향·순환·비교) 추가.
- **왜**: Claude Code만으로는 "AI 코딩 에이전트 지형"을 못 담음. Codex·Manus까지 한 화면에서 비교해야 *써볼 가치*가 상대적으로 보인다. 이름 "what to try"/"ai·pick"은 정체성이 약해 브랜드 필요.
- **핵심 결정·교훈**: CC/Codex는 changelog형(버전블록+기간 드롭다운), Manus는 이벤트형(전폭) — **소스 성격에 맞춰 레이아웃을 분기**. 단일 정적 HTML 유지(빌드 없음)로 배포 마찰 0. nav를 상단바에 통합해 모바일 세로 공간 절약.

## 2026-05-29 — MVP 강화: 효과성 ★ 등급 · i18n · 애널리틱스

- **무엇**: 써볼 기능에 **효과성 3단계 골드 ★ 등급 + 정렬** 도입(점 → ★). **한/영 i18n 토글**, GA4·Search Console·meta description, 시니어 프로덕트 디자이너 리디자인(랜드마크 하이라이트, 모노 SVG topbar).
- **왜**: "다 써볼 만하다"는 신호가 아님 — 등급으로 **우선순위**를 강제해야 큐레이션 가치가 생김. 영어 사용자·검색 유입 대비.
- **핵심 결정·교훈**: 효과성 등급은 자동화가 아니라 **판단의 산물** — Claude가 매 릴리스에서 직접 매김. 상대시간은 "N일 전"으로 통일하고 히트맵 색(빨강→흐림)으로 신선도 표현.

## 2026-05-28 — Claude Code changelog 큐레이션 MVP

- **무엇**: 공식 Claude Code changelog(시간순 raw 목록)를 **3가지 시각으로 재구성**하는 단일 정적 HTML. ① 🎯오늘 써볼 기능 6개(왜 효과적+학습포인트) ② 🧰용도별 8 카테고리 ③ 버전별 changelog 블록(Feature 한 줄·개선/보안/수정 탭 접기). 명령어→공식 docs deep-link(Text Fragment), 며칠전 히트맵.
- **왜**: 매주 1~2개씩 쏟아지는 릴리스에서 *정말 써볼 만한 것*을 raw 목록으로는 가려내기 어렵다. 같은 데이터를 **신호 중심으로 재배치**하면 노이즈가 걸러진다.
- **핵심 결정·교훈**: **매일 05:20 KST GitHub Actions 자동화** — `update_changelog.py`(토큰 0)가 버전 감지·분류·삽입하고, 새 feature 있는 날만 Claude Code Action이 🎯Pick·🧰용도별을 갱신. **구독 토큰(API 키 X)**으로 per-token 과금 0. 대부분의 날은 무료 1단계만 돈다.
- **본질**: 노이즈에서 신호 거르기 + 가치 판단 + 학습/성장. → GitHub Pages → ai.sungd.uk.
