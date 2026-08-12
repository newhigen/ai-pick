# -*- coding: utf-8 -*-
"""화면의 바깥 링크가 성한지 본다. 매일 큐레이션 뒤에 돌린다(경고만, 막지는 않음).

이 사이트는 값의 대부분이 링크다 — 명령어는 공식 문서로, 버전은 패치노트로.
그래서 링크가 조용히 썩으면 화면은 멀쩡한데 쓸모가 없다. 두 가지를 본다.

① 글자 조각 앞에 `#` 이 있나 — 빠지면 조각이 주소 경로가 되어 404 다(2026-08-12 실제로 44개).
② 줄마다 밖으로 나가는 길이 하나는 있나 — 명령어 없는 항목이 링크 없이 남던 적이 있다.
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

# ② 줄마다 나가는 길
ROW = re.compile(r'<div class="(?:it |ci)[^"]*"[^>]*>.*?'
                 r'(?=<div class="(?:it |ci)|<div class="c-day|<p class="foot"'
                 r'|</div><div class="cl">|<div class="cat" |$)', re.S)
rows = ROW.findall(V)
orphan = [r for r in rows if '<a ' not in r]
if orphan:
    bad += len(orphan)
    print(f'★ 밖으로 나가는 길이 없는 줄 {len(orphan)}개')
    for r in orphan[:3]:
        t = re.search(r'<span class="(?:tt|cd)">(.*?)</span>', r, re.S)
        print('   ', re.sub(r'<[^>]+>', '', t.group(1))[:70] if t else '?')

print(f'줄 {len(rows)}개 · 링크 {len(re.findall(chr(104)+"ref=", V))}개 · 걸린 것 {bad}개')

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
