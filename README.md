# ai.sungd.uk

**오늘 뭐 써볼까** — Claude Code·Codex 릴리스에서 오늘 해볼 것을 골라 체크리스트로 준다.
단일 정적 HTML, 빌드 없음. GitHub Pages 가 `main` 루트를 그대로 서빙한다.

🔗 케이스 스터디 → https://resume.sungd.uk/projects/claude-code-tracking

## 왜 만들었나

[공식 changelog](https://code.claude.com/docs/en/changelog)는 시간순 raw 목록이다. 빠짐없지만
매주 릴리스가 1~2개씩 쏟아져 뭐가 정말 써볼 만한지 가려내기 어렵다. 읽을거리가 아니라
**할 일**로 바꿔 두 축으로 세웠다.

1. **새로 나온 것** — 시간순. 줄마다 해볼 것 하나와 체크 칸. 자세히엔 무엇이 바뀌나·좋은 점·해보기
2. **용도별** — 여덟 칸(긴 작업·멀티 세션·PR·비용·UI·플러그인·Hook·모델). 일로 들어가 그 자리에서 쓸 것만

두 화면은 체크 상태를 같이 본다(`localStorage`, 이 브라우저 안에서만). 원본 전체는
공식 패치노트로 링크만 걸고 싣지 않는다.

## 어디를 고치나

```
index.html    전부 (화면·스타일·스크립트 + <div id="data"> 안의 버전블록 321개)
scripts/      매일 도는 갱신 자동화
CNAME · sitemap.xml · robots.txt
```

⚠ `<div id="data">` 는 화면에 안 나오지만 **지우면 안 된다.** 매일 도는 스크립트가
거기에 새 버전을 꽂고 큐레이션이 거기서 원본을 읽는다. 구간 표식(`<!--CC-DATA-->`·
`<!--CX-DATA-->`)도 스크립트가 경계로 쓰므로 그대로 둘 것.

## 매일 도는 갱신

`.github/workflows/daily-update.yml` 이 05:20(KST)에 실행된다. 세 단계인데
**대부분의 날은 1·2단계만 돌아 비용이 0이다.**

1. **버전 수집** (순수 스크립트) — `update_changelog.py`(Claude Code)·`update_codex.py`(Codex stable)
2. **글 수집** — `collect_blog.py` 가 Anthropic·OpenAI 신규 글을 `new_blog.json` 으로
   (화면엔 안 올린다 — 기능이 철회됐는지 알아채는 데만 쓴다)
3. **큐레이션** (새 feature·새 글 있을 때만) — 헤드리스 `claude -p` 가 `curate_prompt.md` 를 따라
   `index.html` 을 직접 고친다

⚠ 3단계가 `index.html` 을 직접 편집한다. 편집 뒤 JS 무결성 검사에 실패하면 자동으로 되돌린다.

### 셋업 (한 번만)

1. [Claude GitHub App](https://github.com/apps/claude) 을 이 repo 에 설치
2. `claude setup-token` (Pro/Max 구독) → OAuth 토큰 발급
3. repo Settings → Secrets → `CLAUDE_CODE_OAUTH_TOKEN` 등록

API 키 대신 구독 토큰을 써서 별도 과금이 없다.

## 라이선스

코드는 MIT. 큐레이션 문구는 대상이 아니다 — `LICENSE` 참고.
다른 사이트는 [sungd.uk](https://sungd.uk) 에서.
