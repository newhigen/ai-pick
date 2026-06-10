# -*- coding: utf-8 -*-
"""3사 blog·news 최신 목록을 훑어, index.html에 아직 없는(카드/분석 미존재) 새 글을 new_blog.json으로.
stage-2(claude -p)가 이 목록을 보고 Blog 사이드바·Manus 카드·뉴스 피드에 배치한다."""
import re,json,subprocess,os
def fetch(u):
    try: return subprocess.run(['curl','-sL','--max-time','15','-A','Mozilla/5.0',u],capture_output=True,text=True,timeout=20).stdout
    except Exception: return ''
html=open('index.html',encoding='utf-8').read()
known=set(re.findall(r'https://(?:claude\.com/blog|(?:www\.)?anthropic\.com/news|openai\.com/index|manus\.im/blog)/[a-z0-9-]+', html))
cand=[]
# Claude (Anthropic) blog
for href in set(re.findall(r'href="(/blog/[a-z0-9-]+)"', fetch('https://claude.com/blog'))):
    if href!='/blog': cand.append('https://claude.com'+href)
# Anthropic news (모델 출시·제품 발표·동향이 /blog 아닌 /news에 올라옴 — Fable 5 등 누락 방지)
for slug in set(re.findall(r'/news/([a-z0-9-]+)', fetch('https://www.anthropic.com/news'))):
    cand.append('https://www.anthropic.com/news/'+slug)
# OpenAI index (Codex·OpenAI 제품/동향 — 뉴스 피드 소스)
for slug in set(re.findall(r'/index/([a-z0-9-]+)', fetch('https://openai.com/news/'))):
    cand.append('https://openai.com/index/'+slug)
# Manus blog (제품 글만)
for slug in set(re.findall(r'/blog/([a-z0-9-]+)', fetch('https://manus.im/blog'))):
    if re.match(r'(manus-|introducing-|deep-dive-)',slug) and 'best-' not in slug and slug not in ('manus-is-hiring',):
        cand.append('https://manus.im/blog/'+slug)
new=[]; seen=set()
for u in cand:
    if u in known or u in seen: continue
    seen.add(u); x=fetch(u)
    t=re.search(r'og:title" content="([^"]*)"',x) or re.search(r'<title>([^<|]*)',x)
    src={'claude.com':'Anthropic','www.anthropic.com':'Anthropic','openai.com':'OpenAI','manus.im':'Manus'}.get(u.split('/')[2],u.split('/')[2])
    new.append({'url':u,'title':(t.group(1).strip() if t else u.split('/')[-1])[:90],'src':src})
new=new[:12]
json.dump(new, open('new_blog.json','w'), ensure_ascii=False, indent=1)
gh=os.environ.get('GITHUB_OUTPUT')
if gh: open(gh,'a').write(f'has_blog={"true" if new else "false"}\n')
print(f"새 blog/news 글 {len(new)}개" + (": "+", ".join(n['title'][:30] for n in new) if new else ""))
