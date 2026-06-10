# -*- coding: utf-8 -*-
"""ai-pick Codex 탭 일일 업데이트.

openai/codex GitHub Releases에서 index.html의 최신 추적(cx*) 버전보다 새로운
**stable** 릴리즈를 가져와 Codex 탭에 version-block을 prepend 한다.
- alpha/beta/rc(prerelease) 제외
- Codex view 슬라이스 안에서만 편집 (Claude Code 탭 오염 방지)
- 변경이 있으면 index.html 갱신 + GITHUB_OUTPUT 플래그, 없으면 멱등

stage-2(헤드리스 claude -p)가 codex-pick 큐레이션을 이어서 처리한다.
"""
import re, json, html as htmllib, urllib.request, sys, os
from datetime import datetime

HTML_PATH = 'index.html'
RELEASES_URL = 'https://api.github.com/repos/openai/codex/releases?per_page=100'

DAYS_KR = ['월', '화', '수', '목', '금', '토', '일']
DAYS_EN = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MON_EN = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ai-pick-codex'})
    last = None
    for _ in range(3):  # GitHub API 일시 5xx/타임아웃 재시도
        try:
            return urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
        except Exception as e:
            last = e
    raise last


def ver_tuple(v):
    return tuple(int(x) for x in v.split('.'))


def md_to_html(s):
    s = re.sub(r'\s*\((#\d+(?:,\s*#\d+)*)\)\s*$', '', s)  # 끝의 (#PR) 참조 제거
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    return s.strip()


def fmt_date(date_str):
    d = datetime.strptime(date_str, '%Y-%m-%d')
    ko = f'{d.month}월 {d.day}일 {DAYS_KR[d.weekday()]}'
    en = f'{MON_EN[d.month]} {d.day} {DAYS_EN[d.weekday()]}'
    return ko, en


def parse_sections(body):
    """release body → {'feature':[...], 'fix':[...]} (## 헤딩 기준 분류)."""
    by = {'feature': [], 'fix': []}
    cur = None
    for ln in body.replace('\r\n', '\n').split('\n'):
        h = re.match(r'^#{1,3}\s*(.+?)\s*$', ln)
        if h:
            t = h.group(1).lower()
            if 'fix' in t or 'bug' in t:
                cur = 'fix'
            elif 'feature' in t or 'new' in t or 'improv' in t or 'enhan' in t:
                cur = 'feature'
            else:
                cur = None  # chore·changelog(원시 커밋 리스트)·기타 → 수집 안 함
            continue
        m = re.match(r'^\s*[-*]\s+(.*)$', ln)
        if m and cur and m.group(1).strip():
            by[cur].append(m.group(1).strip())
    # 헤딩이 전혀 없으면 전체 불릿을 기능으로
    if not by['feature'] and not by['fix']:
        for ln in body.split('\n'):
            m = re.match(r'^\s*[-*]\s+(.*)$', ln)
            if m and m.group(1).strip():
                by['feature'].append(m.group(1).strip())
    return by


def gen_block(ver, by, date):
    feats, fixes = by['feature'], by['fix']
    if not feats and not fixes:
        return ''
    ko, en = fmt_date(date)
    pills = []
    if feats:
        pills.append(f'<span class="pill feature">기능 ×{len(feats)}</span>')
    if fixes:
        pills.append(f'<span class="pill fix">Fix ×{len(fixes)}</span>')
    out = [f'    <div class="version-block" id="cx{ver}" data-date="{date}">',
           f'      <div class="version-head">',
           f'        <span class="ver-badge">v{ver}</span><span class="ver-date" data-en="{en}">{ko}</span><span class="ver-ago"></span>',
           f'        <div class="ver-summary">{"".join(pills)}</div>',
           f'      </div>']
    for f in feats:
        out.append(f'      <div class="entry row-divider" data-type="feature"><span class="pill feature" data-en="Feature">기능</span><span class="e-desc">{md_to_html(f)}</span></div>')
    for f in fixes:
        out.append(f'      <div class="entry row-divider" data-type="fix"><span class="pill fix">Fix</span><span class="e-desc">{md_to_html(f)}</span></div>')
    out.append(f'    </div>')
    return '\n'.join(out)


def main():
    html = open(HTML_PATH, encoding='utf-8').read()

    cs = html.index('<div class="view hidden" data-view="codex">')
    ce = html.index('<div class="view hidden" data-view="manus">')
    codex = html[cs:ce]

    existing = set(re.findall(r'id="cx(\d+\.\d+\.\d+)"', codex))
    if not existing:
        print('ERROR: no codex version blocks found', file=sys.stderr)
        sys.exit(1)
    latest = max(existing, key=ver_tuple)

    try:
        releases = json.loads(fetch(RELEASES_URL))
    except Exception as e:  # 네트워크/일시 API 오류 → CI 실패 대신 멱등 no-op
        print(f'codex releases fetch failed ({e}); skipping this run', file=sys.stderr)
        gh = os.environ.get('GITHUB_OUTPUT')
        if gh:
            open(gh, 'a').write('cx_changed=false\ncx_has_features=false\n')
        return
    rels = []
    for r in releases:
        tag = r.get('tag_name', '')
        m = re.match(r'^rust-v(\d+\.\d+\.\d+)$', tag)  # stable만 (alpha/beta는 -alpha.N 이라 매칭 안됨)
        if not m or r.get('prerelease'):
            continue
        rels.append((m.group(1), r['published_at'][:10], r.get('body') or ''))

    new = [(v, d, b) for v, d, b in rels
           if v not in existing and ver_tuple(v) > ver_tuple(latest)]
    if not new:
        print(f'No new codex versions. Latest tracked: cx{latest}')
        gh = os.environ.get('GITHUB_OUTPUT')
        if gh:
            open(gh, 'a').write('cx_changed=false\ncx_has_features=false\n')
        return

    new.sort(key=lambda x: ver_tuple(x[0]), reverse=True)

    blocks, feat_queue = [], []
    for ver, date, body in new:
        by = parse_sections(body)
        b = gen_block(ver, by, date)
        if b:
            blocks.append(b)
        for it in by['feature']:
            feat_queue.append({'version': ver, 'date': date, 'text': md_to_html(it)})
    if not blocks:
        print('New codex versions had no parseable items.')
        gh = os.environ.get('GITHUB_OUTPUT')
        if gh:
            open(gh, 'a').write('cx_changed=false\ncx_has_features=false\n')
        return

    # 첫 cx version-block 앞에 삽입
    m = re.search(r'^    <div class="version-block" id="cx', codex, flags=re.MULTILINE)
    if not m:
        print('ERROR: codex insertion point not found', file=sys.stderr)
        sys.exit(1)
    idx = m.start()
    codex = codex[:idx] + '\n'.join(blocks) + '\n' + codex[idx:]

    # 범위 헤더 갱신 (codex 슬라이스 내 v0.x만 → CC와 안 겹침)
    newest_ver, newest_date = new[0][0], new[0][1]
    nd = datetime.strptime(newest_date, '%Y-%m-%d')
    codex = re.sub(r'(→ <strong>)v0\.[\d.]+(</strong>)',
                   rf'\g<1>v{newest_ver}\g<2>', codex, count=1)
    rng = f"2025.12.10 – {nd.year}.{nd.month}.{nd.day}"
    codex = re.sub(r'(class="range-dates" data-en=")[^"]*(")', rf'\g<1>{rng}\g<2>', codex, count=1)
    codex = re.sub(r'(<span class="range-dates"[^>]*>)[^<]*(</span>)', rf'\g<1>{rng}\g<2>', codex, count=1)

    html = html[:cs] + codex + html[ce:]
    open(HTML_PATH, 'w', encoding='utf-8').write(html)

    json.dump(feat_queue, open('new-codex-features.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    added = ', '.join(f'v{v}' for v, _, _ in new)
    print(f'Added {len(new)} codex version(s): {added}')
    print(f'New codex features needing judgment: {len(feat_queue)}')

    gh = os.environ.get('GITHUB_OUTPUT')
    if gh:
        with open(gh, 'a') as f:
            f.write('cx_changed=true\n')
            f.write(f'cx_has_features={"true" if feat_queue else "false"}\n')
            f.write(f'cx_added_versions={added}\n')


if __name__ == '__main__':
    main()
