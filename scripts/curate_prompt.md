Agent Edge 사이트(`index.html`, repo: ai-pick) 큐레이션 갱신. 토큰 절약 — 꼭 필요한 최소 편집만. 확신 없으면 아무것도 바꾸지 말 것.

너는 GitHub Actions 러너에서 헤드리스(`claude -p`)로 도는 중이다. **`index.html`을 워킹트리에서 직접 Edit 해라.** 커밋·푸시 금지(워크플로가 처리). 작업 끝나면 그냥 종료.

## 입력 (repo 루트, Read로 읽어라 — 없거나 `[]`면 그 단계 건너뜀)
- `new-features.json` — 새 Claude Code feature (version, date, text).
- `new-codex-features.json` — 새 Codex feature (version=v0.x, date, text).
- `new_blog.json` — 새 blog/news 글 (url, title, src=Anthropic/OpenAI/Manus).

## 공통 원칙
- **각 영역마다 "그 그리드 안의 기존 항목 1개를 그대로 복사 → 값만 교체"** 한다. 마크업 구조·클래스·속성 순서를 절대 바꾸지 말 것.
- 이중 언어: 새/교체 항목엔 영어 `data-en`도 반드시 함께. data-en 안 큰따옴표는 `&quot;`. (`.version-block` 패치노트는 영어 원문이라 data-en 불필요.)
- 한국어 간결한 톤(~함/~음). 영문 직역 금지 — 핵심만 의역. 과장·추측 금지, **검증된 사실만**.
- 효과성 등급: `.pick-tier`에 `t3`(핵심)·`t2`(추천)·`t1`(일반) 클래스를 **반드시** 정확히 부여. **표시는 페이지 JS가 tier별 그룹 헤더(핵심/추천/일반)로 자동 처리** — 별(★) 글리프는 CSS로 숨김. 즉 너는 tier 클래스만 맞추면 되고, 정렬·그룹핑·순서는 sortPicks가 한다(수동 정렬 불필요).
- 편집할 게 없으면 그 영역은 그대로 둔다.

## 1) Claude Code 써볼·용도별 (new-features.json)
- 써볼: `<div class="pick-grid period-grid" data-section="pick" data-period="recent">` 안. "정말 당장 써볼 만한" 게 있을 때만 **기존 카드 1~2개를 복사해 값 교체**(cmd·제목·설명·왜·학습·vtag·data-date·tier). 없으면 그대로.
  - **설명(`<p>`)은 "이게 뭔지" 1줄(≤90자, 2줄 금지)** — 날짜·가격·폴백·세부 조건은 `<p>`에 넣지 말고 왜/학습 또는 클릭 모달로. 날짜는 `data-date`(heatmap)가 이미 표시. cmd 칩에 든 키워드를 설명 끝에 반복 금지.
- 용도별: `<div class="cat-grid period-grid" data-section="cat" data-period="recent">` 안. 새 feature를 적합 카테고리 `<ul class="cat-items">`에 기존 `<li class="cat-item">` 복사해 추가(카테고리당 5개 내외, 과밀 금지).
- 카테고리: 🚀 긴 작업 / 🤖 Subagent·세션 / 📝 PR·리뷰 / 💰 비용·컨텍스트 / 🎨 UI·네비 / 🧩 Plugin·MCP·확장 / 🪝 Hook·모니터링 / 🔒 모델·Enterprise
- 새 슬래시 명령은 `docsMap`(`<script>` 내부)에 경로 추가(모르면 생략 → /commands 폴백).

## 2) Codex 써볼 (new-codex-features.json)
- `<div class="pick-grid period-grid" data-section="codex-pick" data-period="recent">` 안 (CC 탭 아님, **Codex 탭** `data-view="codex"`).
- new-codex-features 중 당장 써볼 만한 게 있을 때만 **기존 codex-pick 카드 1~2개를 복사해 값 교체**. vtag는 `v0.139.0` 형식. 없으면 그대로.
- Codex 명령은 `codex ...`/슬래시. docsMap에 Codex docs 경로 모르면 생략.

## 3) Manus 카드 (new_blog.json 중 src=Manus, 제품 출시·기능만)
- `<div class="view hidden" data-view="manus">` 안 `<div class="news-grid">`에 **기존 `<a class="news-card feat-card">` 복사해 값 교체**(href·tier·h3·p·data-date). 고객사례·채용·법률 글 제외.
- 모달 분석을 주려면 `const ANALYSIS={` 바로 뒤에 그 회사 기존 항목 복사해 추가(co·ico SVG 그대로·tier·date·lead/scn/prin/ctx ko·en·src). 확신 없으면 ANALYSIS 생략하고 카드만 — 카드 href에 ANALYSIS 없으면 그냥 원문 링크로 열림(정상).

## 4) 뉴스 (new_blog.json 중 동향 = 펀딩·인수·파트너십·밸류·벤치마크)
- `<div class="view hidden" data-view="news">` 안 `<div class="news-feed">`에 **기존 `<a class="feed-item">` 복사해 값 교체**: feed-date(KO)+data-en(EN 짧은 날짜), feed-ago `data-date`, src 클래스(`src-anthropic`/`src-openai`/`src-manus`)+이름, feed-title, feed-desc(ko+data-en en), feed-tier.
- **제품 기능 출시는 뉴스 아님** — 그건 위 블로그/Manus/써볼로. 뉴스는 회사 차원 동향만.

## 5) Blog 사이드바 (new_blog.json 중 Anthropic 제품 글)
- 해당 회사 `aside.tool-side`의 `<div class="side-sec">`(h3 "blog") 안에 기존 `<a class="side-feat">` 복사해 추가(href·sf-title·sf-desc). 풍부한 모달 원하면 ANALYSIS 항목도(2번 Manus와 동일 방식). 정렬은 페이지 JS가 date순 자동.

## 6) 철회·중단 감지 (회수된 픽 정리) ★ 중요
새 입력(new_blog.json 뉴스·changelog 텍스트)이 **이전에 픽/모달로 올린 기능·모델의 철회·중단·접근차단·deprecated·superseded·이름변경**을 알릴 때, 그 맥락을 반영한다. (예: "Fable 5 미국 수출통제로 접근 중단" → 기존 Fable 5 ★★★ 픽은 더 이상 "당장 써볼" 대상이 아님.)

- **신호**: 중단/철회/접근 차단/withdrawn/suspended/discontinued/deprecated/sunset/superseded/롤백/이름변경(rename) 등.
- **조치**: 해당하는 기존 `data-section="pick"`/`codex-pick` 카드를 ① **삭제**(완전 불가) 또는 ② tier를 낮추고(`t3`→`t1`) 제목/설명에 상태 표기(예: 제목 끝 "— 중단"). 동시에 그 사건은 **뉴스(§4)** 에 동향으로 올린다.
- **랜드마크**: 중단된 게 현재 랜드마크 배너 대상이면, 페이지 JS가 자동 처리하므로 배너 마크업은 건드리지 말 것. (중단 표시용 `#landmarkBanner.halt` 상태 CSS는 이미 있음 — 랜드마크 감지 로직이 향후 활용.)
- 확신 없으면(정말 회수인지 모호하면) 픽은 그대로 두고 뉴스만 추가.

## 7) 패치노트 기능(feature) 번역 ★
새로 추가된 버전 블록의 **기능(feature) 항목만** 한국어로. (개선·보안·수정은 영어 원문 그대로 — 탭에 접혀 부차적.)

- 대상: `new-features.json`에 있는 각 version에 해당하는 `<div class="version-block" id="v{버전}">`(Codex는 `cx{버전}`) 안의 **`.entry[data-type="feature"] > .e-desc`** 만.
- 방식: `e-desc` 텍스트를 한국어로 의역(핵심만, 간결), **영어 원문은 `data-en`으로 보존**. 예: `<span class="e-desc" data-en="Session titles are now generated in the language of your conversation">세션 제목을 대화 언어로 자동 생성</span>`. `<code>` 등 인라인 태그·구조는 유지.
- improve/security/fix 항목(탭 안 `.coll-item` 등)·이미 번역된 항목·옛 버전은 건드리지 말 것. 새 버전의 feature만.

## 절대 금지
- `.version-block`(패치노트)·월별 그리드(data-period가 recent 아닌 것)·랜드마크 배너·디자인/CSS는 건드리지 마라. 버전 블록은 스크립트가, 랜드마크는 페이지 JS가 자동 처리한다. **단 §7(새 버전 feature `e-desc` 한국어화)만 예외** — e-desc 텍스트만, 구조·클래스·data-type 불변.
- **명백한 플레이스홀더·테스트 엔트리만 건너뛴다** ("Bug fixes and reliability improvements", "Internal infrastructure improvements" 등). 과장된 홍보문구(새 모델 출시 등)는 실제 메이저 발표일 수 있으니 임의로 빼지 말 것 — 새 모델/플래그십 출시는 최우선 t3 픽 후보다.
- 각 영역의 기존 마크업 형식을 절대 깨지 말 것. ANALYSIS의 JS 객체 문법(따옴표·콤마)을 절대 깨지 말 것. 확신 없으면 그 항목은 건너뛴다.
