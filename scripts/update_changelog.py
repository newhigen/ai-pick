#!/usr/bin/env python3
"""
ai-pick 일일 업데이트 스크립트.

index.html의 최신 추적 버전을 확인하고, 그보다 새로운 Claude Code
릴리스가 있으면 changelog를 가져와 분류·HTML 블록 생성 후 맨 위에 삽입한다.

- 데이터: github.com/anthropics/claude-code CHANGELOG.md + Releases API
- 기존 버전 블록은 절대 건드리지 않음 (새 버전만 prepend)
- 변경이 있으면 exit 0 + index.html 갱신, 없으면 그대로 (멱등)

GitHub Actions에서 매일 실행. 변경 여부는 git diff로 판단.
"""
import re, json, html as htmllib, urllib.request, sys
from datetime import datetime, timezone, timedelta

HTML_PATH = 'index.html'
CHANGELOG_URL = 'https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md'
RELEASES_URL = 'https://api.github.com/repos/anthropics/claude-code/releases?per_page=100'

DAYS_KR = ['월', '화', '수', '목', '금', '토', '일']

SECURITY_KW = ['permission', 'sandbox', 'bypass', 'credential', 'auth', 'leak',
               'restrict', 'enforce', 'forceLogin', 'managed setting', 'CVE',
               'allowlist', 'denylist', 'IDOR', 'isolation']
FEATURE_KW = ['Added', 'New ', 'now supports', 'Introduced', 'now lets',
              'Renamed', 'now accepts', 'now offers', 'now provides',
              'now applies', 'now invokes', 'now stays', 'now switches',
              'Added the', 'Added a', 'Added an']
IMPROVE_KW = ['Improved', 'Enhanced', 'faster', 'more efficient', 'now scanned',
              'streaming', 'lower memory', 'reduced', 'optimized',
              'Simplified', 'expanded', 'auto-mode']


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'ai-pick-updater'})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8')


def ver_tuple(v):
    return tuple(int(x) for x in v.split('.'))


def classify(line):
    low = line.lower()
    if line.startswith('Fixed') or line.startswith('Fix '):
        for k in SECURITY_KW:
            if k.lower() in low:
                return 'security'
        return 'fix'
    for k in FEATURE_KW:
        if line.startswith(k):
            return 'feature'
    for k in IMPROVE_KW:
        if k.lower() in low[:50]:
            return 'improve'
    if re.match(r'^\s*[`/]', line):
        return 'feature'
    return 'feature'


def md_to_html(s):
    # 꺾쇠/앰퍼샌드 먼저 escape: CLI 플레이스홀더 <name>·<url> 등이 phantom HTML 태그가 되어 페이지를 깨뜨리는 것 방지
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    return s


def chip_label(item):
    plain = re.sub(r'`([^`]+)`', r'\1', item)
    plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain)
    plain = re.sub(r'\*\*([^*]+)\*\*', r'\1', plain)
    plain = re.sub(r'^Fixed\s+', '', plain, flags=re.IGNORECASE)
    plain = re.sub(r'^[Tt]he\s+', '', plain)
    words = plain.split()
    return ' '.join(words[:8]) + ('…' if len(words) > 8 else '')


def fmt_date(date_str):
    d = datetime.strptime(date_str, '%Y-%m-%d')
    return f'{d.month}월 {d.day}일 {DAYS_KR[d.weekday()]}'


def parse_items(body):
    return [ln[2:].strip() for ln in body.split('\n') if ln.strip().startswith('- ')]


def gen_block(ver, by_type, date):
    feats, imps, secs, fixes = (by_type['feature'], by_type['improve'],
                                by_type['security'], by_type['fix'])
    types = [t for t, items in
             [('feature', feats), ('improve', imps), ('security', secs), ('fix', fixes)]
             if items]
    if not types:
        return ''

    pills = []
    if feats: pills.append(f'<span class="pill feature">기능 ×{len(feats)}</span>')
    if imps:  pills.append(f'<span class="pill improve">개선 ×{len(imps)}</span>')
    if secs:  pills.append(f'<span class="pill security">보안 ×{len(secs)}</span>')
    if fixes: pills.append(f'<span class="pill fix">Fix ×{len(fixes)}</span>')

    out = [f'  <!-- ── v{ver} ── -->',
           f'  <div class="version-block" id="v{ver}" data-types="{" ".join(types)}" data-date="{date}">',
           f'    <div class="version-head">',
           f'      <span class="ver-badge">v{ver}</span><span class="ver-date">{fmt_date(date)}</span><span class="ver-ago"></span>',
           f'      <div class="ver-summary">{"".join(pills)}</div>',
           f'    </div>']

    for f in feats:
        out.append(f'    <div class="entry row-divider" data-type="feature">')
        out.append(f'      <span class="pill feature">기능</span>')
        out.append(f'      <span class="e-desc">{md_to_html(f)}</span>')
        out.append(f'    </div>')

    if imps or secs or fixes:
        out.append(f'    <div class="tabs-container">')
        tabs = []
        if imps:  tabs.append(f'        <div class="tab" data-tab="improve" onclick="toggleTab(this)">⚡ 개선 <span class="tab-count">{len(imps)}</span></div>')
        if secs:  tabs.append(f'        <div class="tab" data-tab="security" onclick="toggleTab(this)">🔒 보안 <span class="tab-count">{len(secs)}</span></div>')
        if fixes: tabs.append(f'        <div class="tab" data-tab="fix" onclick="toggleTab(this)">🐛 수정 <span class="tab-count">{len(fixes)}</span></div>')
        out.append(f'      <div class="tabs-bar">')
        out.append('\n'.join(tabs))
        out.append(f'      </div>')
        out.append(f'      <div class="tab-panels">')
        for tab, items in [('improve', imps), ('security', secs)]:
            if items:
                out.append(f'        <div class="tab-panel" data-tab="{tab}">')
                out.append(f'          <div class="coll-rows">')
                for it in items:
                    out.append(f'            <div class="coll-item"><span class="coll-item-desc">{md_to_html(it)}</span></div>')
                out.append(f'          </div>')
                out.append(f'        </div>')
        if fixes:
            out.append(f'        <div class="tab-panel" data-tab="fix">')
            out.append(f'          <div class="chip-grid">')
            for it in fixes:
                out.append(f'            <span class="chip">{htmllib.escape(chip_label(it))}</span>')
            out.append(f'          </div>')
            out.append(f'        </div>')
        out.append(f'      </div>')
        out.append(f'    </div>')
    out.append(f'  </div>')
    out.append('')
    return '\n'.join(out)


def main():
    html = open(HTML_PATH, encoding='utf-8').read()

    # 기존 추적 버전 집합 + 최신
    existing = set(re.findall(r'id="v(2\.\d+\.\d+)"', html))
    if not existing:
        print('ERROR: no version blocks found in index.html', file=sys.stderr)
        sys.exit(1)
    latest = max(existing, key=ver_tuple)

    # changelog + dates
    changelog = fetch(CHANGELOG_URL)
    releases = json.loads(fetch(RELEASES_URL))
    date_map = {r['tag_name'].lstrip('v'): r['published_at'][:10] for r in releases}

    sections = re.split(r'^## ([\d.]+)\s*$', changelog, flags=re.MULTILINE)
    versions = []
    for i in range(1, len(sections), 2):
        versions.append((sections[i].strip(),
                         sections[i + 1].strip() if i + 1 < len(sections) else ''))

    # 최신보다 새롭고 아직 없는 버전
    new = []
    for ver, body in versions:
        if ver in existing:
            continue
        if ver not in date_map:
            continue
        if ver_tuple(ver) <= ver_tuple(latest):
            continue
        new.append((ver, body, date_map[ver]))

    if not new:
        print(f'No new versions. Latest tracked: v{latest}')
        import os
        gh_out = os.environ.get('GITHUB_OUTPUT')
        if gh_out:
            with open(gh_out, 'a') as f:
                f.write('changed=false\n')
                f.write('has_features=false\n')
        return

    new.sort(key=lambda x: ver_tuple(x[0]), reverse=True)  # 최신 먼저

    blocks = []
    for ver, body, date in new:
        by = {'feature': [], 'improve': [], 'security': [], 'fix': []}
        for item in parse_items(body):
            by[classify(item)].append(item)
        b = gen_block(ver, by, date)
        if b:
            blocks.append(b)
    if not blocks:
        print('New versions had no parseable items.')
        return

    # 첫 version-block 앞에 삽입
    m = re.search(r'^  <!-- ── v[\d.]+ ── -->', html, flags=re.MULTILINE)
    if not m:
        m = re.search(r'^  <div class="version-block"', html, flags=re.MULTILINE)
    if not m:
        print('ERROR: insertion point not found', file=sys.stderr)
        sys.exit(1)
    idx = m.start()
    html = html[:idx] + '\n'.join(blocks) + '\n' + html[idx:]

    # 헤더 범위 갱신: 두 번째 strong(최신 버전), 날짜 끝
    newest_ver = new[0][0]
    newest_date = new[0][2]
    nd = datetime.strptime(newest_date, '%Y-%m-%d')
    html = re.sub(
        r'(<p class="range"><strong>v[\d.]+</strong> → <strong>)v[\d.]+(</strong>)',
        rf'\g<1>v{newest_ver}\g<2>', html)
    # 날짜 범위 끝 (… – M월 D일) 형태 갱신: 마지막 "– N월 N일" 부분 교체
    html = re.sub(
        r'(– )\d+월\s*\d+일',
        rf'\g<1>{nd.month}월 {nd.day}일', html, count=1)
    # 영어 날짜(range-dates data-en)도 갱신: 시작 Sep 29, 2025 고정, 끝만 변동
    EN_MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    html = re.sub(
        r'(class="range-dates" data-en=")[^"]*(")',
        rf'\g<1>Sep 29, 2025 – {EN_MON[nd.month-1]} {nd.day}\g<2>', html, count=1)

    # 동기화 타임스탬프 갱신 (KST)
    kst = timezone(timedelta(hours=9))
    stamp = datetime.now(kst).strftime('%Y-%m-%d %H:%M')
    html = re.sub(r'<!--SYNC-->.*?<!--/SYNC-->',
                  f'<!--SYNC-->{stamp}<!--/SYNC-->', html)

    open(HTML_PATH, 'w', encoding='utf-8').write(html)
    added = ', '.join(f'v{v}' for v, _, _ in new)
    print(f'Added {len(new)} version(s): {added}')

    # 새 feature 목록을 판단 큐로 기록 (Claude 단계용)
    feat_queue = []
    for ver, body, date in new:
        for item in parse_items(body):
            if classify(item) == 'feature':
                feat_queue.append({'version': ver, 'date': date, 'text': item})
    with open('new-features.json', 'w', encoding='utf-8') as f:
        json.dump(feat_queue, f, ensure_ascii=False, indent=2)
    print(f'New features needing judgment: {len(feat_queue)}')

    # GitHub Actions 출력 플래그
    import os
    gh_out = os.environ.get('GITHUB_OUTPUT')
    if gh_out:
        with open(gh_out, 'a') as f:
            f.write(f'changed=true\n')
            f.write(f'has_features={"true" if feat_queue else "false"}\n')
            f.write(f'added_versions={added}\n')


if __name__ == '__main__':
    main()
