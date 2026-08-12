「오늘 뭐 써볼까」(`index.html`, ai.sungd.uk) 큐레이션 갱신. 토큰 절약 — 꼭 필요한 최소 편집만. 확신 없으면 아무것도 바꾸지 말 것.

너는 GitHub Actions 러너에서 헤드리스(`claude -p`)로 도는 중이다. **`index.html`을 워킹트리에서 직접 Edit 해라.** 커밋·푸시 금지(워크플로가 처리). 작업 끝나면 그냥 종료.

## 화면은 둘뿐이다

| 화면 | 축 | 어디 |
|---|---|---|
| 새로 나온 것 | 시간 — 언제 나왔나 | `<div class="tab on" id="new">` 안 `.t-cc` / `.t-cx` |
| 용도별 | 일 — 무슨 일 할 때 | `<div class="tab" id="use">` 안 `.t-cc` / `.t-cx` |

Manus·뉴스·블로그 화면은 **없앴다**. 그런 내용은 이제 아무 데도 넣지 마라.

`<div id="data">` 는 화면에 안 나오는 자료칸이다. 버전블록·명령어 문서표가 들어 있고 **여기는 절대 손대지 마라** — 버전블록은 스크립트(추가)와 전용 번역 스텝이 다룬다.

## 입력 (repo 루트, Read로 읽어라 — 없거나 `[]`면 그 단계 건너뜀)
- `new-features.json` — 새 Claude Code feature (version, date, text).
- `new-codex-features.json` — 새 Codex feature (version=v0.x, date, text).
- `new_blog.json` — 새 blog/news 글. **화면에 올리지 않는다.** 철회·중단 감지(§4)에만 쓴다.

## 공통 원칙
- **기존 줄 하나를 그대로 복사해 값만 교체한다.** 마크업 구조·클래스·속성 순서를 절대 바꾸지 말 것.
- 한국어 간결한 톤(~함/~음). 영문 직역 금지 — 핵심만 의역. 과장·추측 금지, **검증된 사실만**.
- 편집할 게 없으면 그 영역은 그대로 둔다.
- `data-en` 은 더 이상 쓰지 않는다(영어 전환 기능을 뺐다). 새 줄에 넣지 마라.

## 체크 키 — 두 화면을 잇는 끈 ★
줄마다 `data-k="도구:명령어첫낱말@버전"` 이 있다. 이 키가 같아야 **새로 나온 것에서 체크한 게 용도별에도 뜬다.**

- 도구는 `cc` 또는 `cx`, 버전은 `v` 없이 (`cc:/context@2.1.216`).
- **명령어의 첫 낱말만** 쓴다 — `/context 초과 경고` 도 `/context` 다. 공백·`·`·`→`·`,` 앞에서 끊는다.
- 같은 기능을 두 화면에 넣을 땐 **키가 반드시 같아야 한다.** 이름을 다르게 적어도 키는 같게.
- 한 화면 안에서 키가 겹치면(서로 다른 기능인데 첫 낱말·버전이 같음) 그때만 명령어를 통째로 쓴다.

## 1) 새로 나온 것 — Claude Code (new-features.json)
`<div class="tab on" id="new">` 안 `<div class="tw t-cc on">` 의 `.box0`.

- **날짜 줄이 먼저다.** 그 날짜의 `<div class="c-day">` 가 이미 있으면 그 아래에 줄을 넣고, 없으면 위쪽 날짜 줄을 복사해 새로 만든다(날짜·요일·`<em>` 상대주·버전 링크 교체). **최신 날짜가 위**다.
- 줄은 이 꼴이다. 기존 `.it` 하나를 복사해 값만 갈아라.

```
<div class="it t2 nw" data-t="제목" data-k="cc:/foo@2.1.230"><div class="row">
<span class="star">*</span><span class="sev">추천</span>
<button class="box" data-off="[x]">[ ]</button>
<span class="cmd"><a href="…" target="_blank" rel="noopener noreferrer" title="/foo 공식 문서">/foo</a></span>
<span class="tt">제목</span><span class="ds">좋은 점</span><span class="dt">8.9</span></div>
<div class="det">…자세히…</div></div>
```

- `t3`=핵심 `t2`=추천 `t1`=일반, `.sev` 글자도 같이 맞춘다. `nw` 는 새로 들어온 것 표시(`.star` 의 `*` 와 짝).
- `.dt` 는 `월.일`, `data-t` 는 `.tt` 와 같은 글.
- **`.ds` 는 좋은 점을 그대로 옮긴 것**이다 — 자세히의 「좋은 점」과 같은 문장을 쓴다.
- **명령어 링크는 그 기능이 적힌 자리로 보낸다.** 순서대로 따진다.
  1. `<div id="data">` 안 `<script type="application/json" id="docsmap">` 에 그 명령의 전용 문서 경로가 있으면 그걸 쓴다.
  2. 없으면 **공식 패치노트의 그 줄**로 — `https://code.claude.com/docs/en/changelog#:~:text=<영어 원문 앞 6~9낱말을 percent-encode>`.
     원문은 그 버전의 `.version-block` 안 `.e-desc` 의 `data-en`(없으면 본문)에 있다.
     ⚠ **활자 따옴표(’)·`<code>` 태그가 섞이면 안 걸린다** — 태그를 벗기고, ASCII 아닌 글자가 나오면 그 앞에서 끊는다.
  3. 조각을 못 만들겠으면 그 버전 앵커(`changelog#2-1-230`)로 물러선다.
  `/overview`·`/commands` 같은 일반 페이지로 보내지 마라 — 그 기능 설명이 아니다.

### 자세히(`.det`) — 네 줄, 순서 고정
```
<p><span class="dk">무엇이 바뀌나</span>…</p>
<p><span class="dk">좋은 점</span>…</p>
<p><span class="dk">해보기</span>…</p>
<p><span class="dk">학습</span>…</p>
```
- **무엇이 바뀌나**: 이게 뭔지 한 줄(≤90자). 날짜·가격·조건은 여기 말고 아래로.
- **좋은 점**: 왜 쓸모 있나. 제목을 딴 말로 되풀이하지 마라.
- **해보기 — 반드시 넣는다.** 세 조건을 모두 만족해야 한다.
  ① **동사로 끝난다**(…해본다/…돌려본다/…센다) ② **한 번에 끝난다**(한 세션·한 명령 분량) ③ **끝났는지 스스로 판단된다**(무엇을 보면 됐는지가 문장 안에 있다).
  - 좋음: `codex --approve-for-me 로 다음 작업을 한 번 돌리고, 승인 클릭이 몇 번 줄었는지 센다.`
  - 나쁨: `요금, /fast 토글, Opus 5 vs Sonnet 5 선택 기준` — 이건 할 일이 아니라 목차다.
  - 무엇을 해볼지 정말 모르겠으면 **그 항목은 픽에서 빼라.** 해볼 수 없는 것은 「새로 나온 것」이 아니다.
- **학습**: 곁들여 알아둘 것. 없으면 그 `<p>` 를 통째로 뺀다.
- 명령·플래그는 `<code>` 로 verbatim.

## 2) 새로 나온 것 — Codex (new-codex-features.json)
`<div class="tw t-cx">` 안. 마크업·규칙은 §1과 같고 이것만 다르다.

- 키는 `cx:…@0.148.0` (`v` 없이).
- 버전 링크는 `https://github.com/openai/codex/releases/tag/rust-v0.148.0`.
- 명령어 링크도 그 릴리스의 그 줄로 — `…/tag/rust-v0.148.0#:~:text=<영어 원문 앞 낱말>`.
  `https://developers.openai.com/codex/` 같은 첫 페이지로 보내지 마라.
- **Codex 픽에도 자세히 네 줄을 다 채운다.** 예전엔 한 줄짜리였는데 이제 Claude Code 와 같은 대접이다.

## 3) 용도별 (두 도구 모두)
`<div class="tab" id="use">` 안, 여덟 칸 중 맞는 `<div class="cat" id="u-cc-N">` 에 넣는다.

칸: 긴 작업 맡기기 / Subagent · 멀티 세션 / PR · 코드 리뷰 / 비용 · 토큰 / 일상 UI · 네비 / Plugin · MCP · 확장 / Hook · 모니터링 / 모델 · Enterprise

```
<div class="ci" data-k="cc:/foo@2.1.230"><button class="box" data-off="[x]">[ ]</button>
<span class="cmd"><a href="…" …>/foo</a></span>
<span class="cd">무엇을 하나</span>
<a class="cv" href="https://code.claude.com/docs/en/changelog#2-1-230" …>v2.1.230</a></div>
```

- 칸 머리(`.cathead`)의 개수 `<b>N</b>` 과 위쪽 칸 목록(`.catnav`)의 `<span class="n">N</span>` 을 **같이 올려라.** 안 맞으면 눈에 띈다.
- 일곱 번째부터는 접히므로 새 줄에 `over` 클래스를 붙인다 — `<div class="ci over" …>`. 칸의 앞 여섯 개만 `over` 가 없다.
- 한 칸에 너무 몰리지 않게(칸당 25개 안쪽).
- **§1·§2 에서 넣은 것과 같은 기능이면 `data-k` 를 똑같이 맞춰라.**

## 4) 철회·중단 감지 ★
새 입력이 **이전에 올린 기능·모델의 철회·중단·접근차단·deprecated·superseded·이름변경**을 알리면 반영한다.

- **신호**: 중단/철회/접근 차단/withdrawn/suspended/discontinued/deprecated/sunset/superseded/롤백/이름변경.
- **조치**: 해당 줄을 ① **삭제** 또는 ② 등급을 낮추고(`t3`→`t1`, `.sev` 도) 제목 끝에 상태 표기(예: "— 중단").
- 확신 없으면(정말 회수인지 모호하면) 그대로 둔다.

## 절대 금지
- `<div id="data">` 안(버전블록·문서표) 은 **일절 건드리지 마라.**
- 상단바·CSS·`<script>` 는 건드리지 마라.
- **명백한 플레이스홀더만 건너뛴다** ("Bug fixes and reliability improvements", "Internal infrastructure improvements" 등). 새 모델·플래그십 출시는 임의로 빼지 말 것 — 최우선 `t3` 후보다.
- 마크업 형식을 깨지 말 것. 확신 없으면 그 항목은 건너뛴다.
