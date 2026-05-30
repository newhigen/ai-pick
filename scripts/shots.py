# -*- coding: utf-8 -*-
"""주요 화면(5탭 + blog 분석 모달)을 PC/모바일로 캡처 → docs/screenshots/.
사용: python3 scripts/shots.py   (로컬 맥 + 시스템 Chrome 기준)
주요 UI 변경 후 실행해 스크린샷을 최신화한다."""
import os
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='file://'+os.path.join(ROOT,'index.html')
D=os.path.join(ROOT,'docs','screenshots')+os.sep
os.makedirs(D, exist_ok=True)
VIEWS=['home','cc','codex','manus','news']
def launch(p):
    try: return p.chromium.launch(channel='chrome')
    except Exception: return p.chromium.launch()
def shoot(pg, suffix):
    for v in VIEWS:
        pg.evaluate(f"switchView('{v}')"); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{D}{v}_{suffix}.png')
    # 분석 모달 (cc 사이드바 Managed Agents)
    pg.evaluate("switchView('cc')"); pg.wait_for_timeout(300)
    try:
        pg.click("a.side-feat:has-text('Managed Agents')", force=True); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{D}modal_{suffix}.png'); pg.evaluate("closeSheet&&closeSheet()")
    except Exception as e: print('modal skip:', e)
with sync_playwright() as p:
    b=launch(p)
    ctx=b.new_context(viewport={'width':1280,'height':900}, device_scale_factor=2)
    pg=ctx.new_page(); pg.goto(URL, wait_until='networkidle'); pg.wait_for_timeout(700)
    shoot(pg,'pc'); ctx.close()
    ctx2=b.new_context(**p.devices['iPhone 13'])
    pg2=ctx2.new_page(); pg2.goto(URL, wait_until='networkidle'); pg2.wait_for_timeout(700)
    shoot(pg2,'mobile'); b.close()
print(f"✅ 캡처 완료 → {D} (5탭+모달 × PC/모바일 = 12장)")
