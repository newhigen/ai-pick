# -*- coding: utf-8 -*-
"""Anthropic·OpenAI blog·news 최신 목록을 훑어 아직 index.html 에 없는 새 글을 new_blog.json 으로.
화면엔 안 올린다 — 큐레이션이 철회·중단 감지(기능이 회수됐는지)에만 쓴다."""
import re,json,subprocess,os
def fetch(u):
    try: return subprocess.run(['curl','-sL','--max-time','15','-A','Mozilla/5.0',u],capture_output=True,text=True,timeout=20).stdout
    except Exception: return ''
html=open('index.html',encoding='utf-8').read()
known=set(re.findall(r'https://(?:claude\.com/blog|(?:www\.)?anthropic\.com/news|openai\.com/index)/[a-z0-9-]+', html))
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
new=[]; seen=set()
for u in cand:
    if u in known or u in seen: continue
    seen.add(u); x=fetch(u)
    t=re.search(r'og:title" content="([^"]*)"',x) or re.search(r'<title>([^<|]*)',x)
    src={'claude.com':'Anthropic','www.anthropic.com':'Anthropic','openai.com':'OpenAI'}.get(u.split('/')[2],u.split('/')[2])
    new.append({'url':u,'title':(t.group(1).strip() if t else u.split('/')[-1])[:90],'src':src})
new=new[:12]
json.dump(new, open('new_blog.json','w'), ensure_ascii=False, indent=1)
gh=os.environ.get('GITHUB_OUTPUT')
if gh: open(gh,'a').write(f'has_blog={"true" if new else "false"}\n')
print(f"새 blog/news 글 {len(new)}개" + (": "+", ".join(n['title'][:30] for n in new) if new else ""))
