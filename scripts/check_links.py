# -*- coding: utf-8 -*-
"""화면의 바깥 링크가 성한지 본다. 매일 큐레이션 뒤에 돌린다(경고만, 막지는 않음).

밖으로 나가는 길은 버전 링크 하나로 모았다 — 새로 나온 것은 날짜줄의 `.vl`,
용도별은 줄 오른쪽 끝의 `.cv`. 명령어는 링크가 아니라 글자다(2026-08-13).
그 길이 조용히 빠지면 화면은 멀쩡한데 원문에 닿을 수가 없다.

① 글자 조각 앞에 `#` 이 있나 — 빠지면 조각이 주소 경로가 되어 404 다(2026-08-12 실제로 44개).
② 날짜줄마다 버전 링크가 있나 · 용도별 줄마다 `.cv` 가 있나.
③ (--net 일 때만) 주소가 정말 열리나.
"""
import re, sys, subprocess, collections, concurrent.futures as cf

HTML = 'index.html'
h = open(HTML, encoding='utf-8').read()
V = h[:h.index('<!-- ══ 자료 ══')] if '<!-- ══ 자료 ══' in h else h
bad = 0

# ① 조각 앞의 #
no_hash = re.findall(r'href="(https://[^"#]*?[^#]:~:text=[^"]*)"', V)
if no_hash:
    bad += len(no_hash)
    print(f'★ 조각 앞에 # 이 없는 주소 {len(no_hash)}개 — 그대로면 404 다')
    for u in no_hash[:5]:
        print('   ', u[:110])

# ② 밖으로 나가는 길
ROW = re.compile(r'<div class="(?:it |ci)[^"]*"[^>]*>.*?'
                 r'(?=<div class="(?:it |ci)|<div class="c-day|<p class="foot"'
                 r'|</div><div class="cl">|<div class="cat" |$)', re.S)
rows = ROW.findall(V)

days = re.findall(r'<div class="c-day"[^>]*>.*?</div>', V, re.S)
dumb = [d for d in days if 'class="vl"' not in d]
if dumb:
    bad += len(dumb)
    print(f'★ 버전 링크가 없는 날짜줄 {len(dumb)}개 — 그 아래 줄들은 원문에 닿을 길이 없다')
    for d in dumb[:3]:
        print('   ', re.sub(r'<[^>]+>', ' ', d).strip()[:60])

ci = [r for r in rows if r.startswith('<div class="ci')]
noc = [r for r in ci if 'class="cv"' not in r]
if noc:
    bad += len(noc)
    print(f'★ 버전 링크가 없는 용도별 줄 {len(noc)}개')
    for r in noc[:3]:
        t = re.search(r'<span class="cd">(.*?)</span>', r, re.S)
        print('   ', re.sub(r'<[^>]+>', '', t.group(1))[:70] if t else '?')

print(f'줄 {len(rows)}개 · 날짜줄 {len(days)}개 · 링크 {len(re.findall(chr(104)+"ref=", V))}개'
      f' · 걸린 것 {bad}개')

# ③ 실제로 열리나
if '--net' in sys.argv:
    bases = sorted({u.split('#')[0] for u in re.findall(r'href="(https://[^"]*)"', V)})

    def code(u):
        return u, subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-L',
             '--max-time', '25', '-A', 'Mozilla/5.0', u],
            capture_output=True, text=True).stdout.strip()

    cnt = collections.Counter()
    with cf.ThreadPoolExecutor(8) as ex:
        for u, c in ex.map(code, bases):
            cnt[c] += 1
            if c != '200':
                bad += 1
                print(f'★ {c}  {u}')
    print(f'주소 {len(bases)}개 확인 — {dict(cnt)}')

sys.exit(0 if bad == 0 else 1)
