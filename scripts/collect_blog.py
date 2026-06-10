# -*- coding: utf-8 -*-
"""3사 blog 최신 목록을 훑어, index.html에 아직 없는(분석/카드 미존재) 새 글을 new_blog.json으로."""
import re,json,subprocess,sys
def fetch(u):
    try: return subprocess.run(['curl','-sL','--max-time','15','-A','Mozilla/5.0',u],capture_output=True,text=True,timeout=20).stdout
    except Exception: return ''
html=open('index.html',encoding='utf-8').read()
known=set(re.findall(r'https://(?:claude\.com/blog|(?:www\.)?anthropic\.com/news|openai\.com/index|manus\.im/blog)/[a-z0-9-]+', html))
cand=[]
# Claude blog
for href in set(re.findall(r'href="(/blog/[a-z0-9-]+)"', fetch('https://claude.com/blog'))):
    if href!='/blog': cand.append('https://claude.com'+href)
# Anthropic news (모델 출시·제품 발표가 /blog 아닌 /news에 올라옴 — Fable 5 등 누락 방지)
for slug in set(re.findall(r'/news/([a-z0-9-]+)', fetch('https://www.anthropic.com/news'))):
    cand.append('https://www.anthropic.com/news/'+slug)
# Manus blog (제품 글만)
for slug in set(re.findall(r'/blog/([a-z0-9-]+)', fetch('https://manus.im/blog'))):
    if re.match(r'(manus-|introducing-|deep-dive-)',slug) and 'best-' not in slug and slug not in ('manus-is-hiring',):
        cand.append('https://manus.im/blog/'+slug)
new=[]; seen=set()
for u in cand:
    if u in known or u in seen: continue
    seen.add(u); x=fetch(u)
    t=re.search(r'og:title" content="([^"]*)"',x) or re.search(r'<title>([^<|]*)',x)
    new.append({'url':u,'title':(t.group(1).strip() if t else u.split('/')[-1])[:80],'src':u.split('/')[2]})
new=new[:8]
json.dump(new, open('new_blog.json','w'), ensure_ascii=False, indent=1)
print(f"새 blog 글 {len(new)}개" + (": "+", ".join(n['title'][:30] for n in new) if new else ""))
