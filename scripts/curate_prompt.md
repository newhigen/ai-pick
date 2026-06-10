Agent Edge 사이트(`index.html`, repo: ai-pick) 큐레이션 갱신. 토큰 절약 — 꼭 필요한 최소 편집만. 확신 없으면 아무것도 바꾸지 말 것.

너는 GitHub Actions 러너에서 헤드리스(`claude -p`)로 도는 중이다. **`index.html`을 워킹트리에서 직접 Edit 해라.** 커밋·푸시 금지(워크플로가 처리). 작업 끝나면 그냥 종료.

## 입력 (repo 루트, Read로 읽어라)
- `new-features.json` — 이번에 추가된 새 feature 목록 (version, date, text).
- `new_blog.json` — (있으면) 새 blog 글 목록. 없거나 `[]`면 blog 단계 건너뜀.

## 구조 (반드시 이 selector 안에서만 편집)
- 써볼 기능 최근(CC 탭 `data-view="cc"` 안): `<div class="pick-grid period-grid" data-section="pick" data-period="recent">` (월별 `data-period`는 절대 건드리지 말 것)
- 용도별 최근: `<div class="cat-grid period-grid" data-section="cat" data-period="recent">`

## 할 일 (보수적으로)
1. **써볼 기능 (recent pick-grid)** — new-features 중 "정말 당장 써볼 만한" 것이 있을 때만 기존 카드 1~2개와 교체. 없으면 그대로 둠.
   카드 형식 (효과성 ★ 등급 포함 — t3 핵심/t2 추천/t1 일반, 우상단):
   ```
   <div class="pick-card" onclick="openDoc(this)" data-date="YYYY-MM-DD">
     <div class="pick-tier t3" title="핵심 — 워크플로우를 크게 바꿈">★★★</div>
     <div class="cmd">/명령</div>
     <h3>짧은 제목</h3>
     <p>한 줄 설명.</p>
     <div class="pick-meta">
       <div class="pick-why"><strong>왜?</strong> 무엇을 더 잘/효과적으로</div>
       <div class="pick-check"><strong>학습:</strong> 써보며 확인할 포인트</div>
     </div>
     <div class="ver"><span class="vtag">v2.1.XXX</span><span class="dag"></span></div>
   </div>
   ```
   등급 기준: t3(★★★)=새 모델/패러다임·핵심 워크플로우, t2(★★☆)=확실히 유용, t1(★☆☆)=소소한 편의. recent는 효과성 높은 순(t3→t1) 좌→우 정렬 유지.
2. **용도별 (recent cat-grid)** — 새 feature를 적합 카테고리 `<ul class="cat-items">`에 추가 (카테고리당 과밀 금지, 5개 내외):
   ```
   <li class="cat-item" onclick="openDoc(this)"><span class="cat-cmd">명령</span><span class="cat-desc">짧은 설명</span><span class="cat-ver">v2.1.XXX</span></li>
   ```
   카테고리: 🚀 긴 작업 / 🤖 Subagent·세션 / 📝 PR·리뷰 / 💰 비용·컨텍스트 / 🎨 UI·네비 / 🧩 Plugin·MCP·확장 / 🪝 Hook·모니터링 / 🔒 모델·Enterprise

## 이중 언어 (필수)
카드를 추가·교체할 때 영어 `data-en` 속성도 반드시 함께 넣어라 (사이트가 KO/EN 토글 지원):
- h3: `<h3 data-en="English title">한글 제목</h3>`
- p: `<p data-en="English desc">한글 설명</p>`
- pick-why: `<div class="pick-why" data-en="<strong>Why</strong> English"><strong>왜?</strong> 한글</div>`
- pick-check: `<div class="pick-check" data-en="<strong>Learn:</strong> English"><strong>학습:</strong> 한글</div>`
- cat-desc: `<span class="cat-desc" data-en="English">한글</span>`
data-en 안의 큰따옴표는 `&quot;` 로 이스케이프. 패치노트(`.version-block`)는 영어 원문이라 data-en 불필요.

## 절대 금지
- 버전 블록(`.version-block`)·월별 그리드(data-period가 recent 아닌 것)·랜드마크는 건드리지 마라. 버전 목록은 스크립트가, 랜드마크는 페이지 JS가 자동 처리한다.
- **편집은 오직 CC 탭(`data-view="cc"`)에만.** Codex 탭(`data-view="codex"`, 그리드 `data-section="codex-pick"`)·Manus 탭은 자동화 대상이 아니니 절대 건드리지 마라.
- 디자인/CSS 변경 금지. 마크업 형식 그대로.
- **가짜·테스트로 의심되는 changelog 엔트리는 픽하지 마라** (실존하지 않는 모델명·과장된 홍보문구 등). 의심되면 건너뛴다.

## 새 blog 글 분석 (new_blog.json — 있을 때만)
new_blog.json 목록 중 **당장 써볼 제품 기능·출시만** 선별(고객사례·"How X uses"·보안가이드·채용·법률 글은 제외):
- `const ANALYSIS={` 바로 뒤에 항목 추가. 형식은 같은 회사 기존 항목을 복사해 값만 교체 — co, ico(같은 회사 ico SVG 그대로 복붙), tier, date, lead_ko/lead_en, scn_ko/scn_en, prin_ko/prin_en, ctx_ko/ctx_en, src. scn=효과성 시나리오, prin=원리(어떻게·왜), ctx=맥락(트렌드·기존기술 접목). 과장·추측 금지, 근거 있는 톤.
- 구조가 뚜렷하면 diagram(dg-node/dg-arr 형식) 포함. 해당 회사 사이드바 side-sec "blog" 또는 Manus 탭에 카드 1개 추가.
- 제품 기능이 아니거나 확신 없으면 추가하지 말 것. ANALYSIS의 JSON 형식을 절대 깨지 말 것.

## 규칙
- 한국어, 간결한 톤(~함/~음). 영문 직역 금지 — 핵심만 의역.
- 새 슬래시 명령은 `docsMap`(`<script>` 내부)에 경로 추가 (모르면 생략 → /commands 폴백).
- 편집할 게 없으면 아무것도 바꾸지 말고 종료.
