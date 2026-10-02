from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,json,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=True);page=browser.new_page(viewport={'width':1366,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/');page.wait_for_function('document.querySelectorAll("[data-language]").length===12')
  expected=['ViewAndConvert','PipeSaver','BestSection','EZNesting','LaymanCad2D']
  assert page.locator('.tool-card').count()==10
  for i,repo in enumerate(expected):assert page.locator('.tool-card').nth(i).get_attribute('href')==f'https://guizlass-afk.github.io/{repo}/'
  assert not page.locator('.quality-links a').first.is_visible()
  page.locator('.quality summary').click();assert page.locator('.quality-links a').count()==10
  for tool in ['ppap','apqp','dfmea','pfmea','control','flow','cep','msa','why','ishikawa']:
   assert page.locator(f'.quality-links a[href="https://guizlass-afk.github.io/QualityToolbox/#{tool}"]').is_visible()
  translations=page.evaluate('FactoryTranslations');assert len(translations)==12
  for code,values in translations.items():
   assert values.keys()==translations['pt-BR'].keys() and all(values.values())
   page.locator('#languageButton').click();page.locator(f'[data-language="{code}"]').click()
   assert page.locator('html').get_attribute('lang')==code
   assert page.locator('html').get_attribute('dir')==('rtl' if code=='ar-SA' else 'ltr')
   for width,height in [(1366,950),(768,900),(390,844),(320,740)]:
    page.set_viewport_size({'width':width,'height':height})
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(code,width)
    assert page.locator('.tool-card').first.bounding_box()['height']>=200
   if code in ['pt-BR','ar-SA']:
    page.set_viewport_size({'width':1366,'height':950});page.screenshot(path=str(Path(os.environ['TEMP'])/f'factory-{code}.png'),full_page=True)
  page.locator('#languageButton').click();page.locator('[data-language="en-US"]').click();page.reload();assert page.locator('html').get_attribute('lang')=='en-US'
  page.locator('#languageButton').focus();page.keyboard.press('ArrowDown');assert page.locator('#languageMenu').is_visible();page.keyboard.press('End');assert page.locator('[data-language="ja-JP"]').evaluate('e=>e===document.activeElement');page.keyboard.press('Escape');assert page.locator('#languageMenu').is_hidden()
  # Exercise real click handling while preventing navigation out of the local test.
  page.locator('.tool-card').first.evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.tool-card').first.click();assert page.evaluate("localStorage.getItem('viewconvert-language')")=='en-US'
  page.locator('.tool-card.layman').evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.tool-card.layman').click();assert page.evaluate("localStorage.getItem('laymancad-language')")=='en-US'
  page.locator('.quality summary').click()
  page.locator('.quality-links a').first.evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.quality-links a').first.click();assert page.evaluate("localStorage.getItem('qualitytoolbox-language')")=='en-US'
  page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(Path(os.environ['TEMP'])/'factory-mobile.png'),full_page=True)
  assert page.locator('.tool-card.bolt').get_attribute('href')=='https://guizlass-afk.github.io/BoltEncyclopedia/'
  page.locator('.tool-card.bolt').evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.tool-card.bolt').click();assert page.evaluate("localStorage.getItem('boltencyclopedia-language')")=='en-US'
  assert page.locator('.tool-card.gear').get_attribute('href')=='https://guizlass-afk.github.io/GearGenerator/'
  page.locator('.tool-card.gear').evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.tool-card.gear').click();assert page.evaluate("localStorage.getItem('geargenerator-language')")=='en-US'
  assert page.locator('.tool-card.unit').get_attribute('href')=='https://guizlass-afk.github.io/UnitConverter/'
  page.locator('.tool-card.unit').evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.tool-card.unit').click();assert page.evaluate("localStorage.getItem('unitconverter-language')")=='en-US'
  assert page.locator('.tool-card.material').get_attribute('href')=='https://guizlass-afk.github.io/MaterialCodex/'
  page.locator('.tool-card.material').evaluate("el=>el.addEventListener('click',e=>e.preventDefault())")
  page.locator('.tool-card.material').click();assert page.evaluate("localStorage.getItem('materialcodex-language')")=='en-US'
  assert not errors,errors
  # Static links and Portuguese descriptions work even when JavaScript is disabled.
  basic=browser.new_context(java_script_enabled=False).new_page();basic.goto(f'http://127.0.0.1:{server.server_port}/');assert basic.locator('.tool-card').count()==10
  browser.close();print('PASS: nine direct links plus ten quality tools, 12 complete languages, four viewport sizes, RTL, keyboard, persistence, language handoff and no-JS navigation.')
finally:server.shutdown()
