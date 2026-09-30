"""Run with the five repositories beside one another in the shared Projects folder."""
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Thread
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright
import os,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[2]
FOLDERS=['Factory Toolbox','View and Convert','Pipesaver','Best Section','EZNesting']
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=True)
  for folder in FOLDERS:
   context=browser.new_context(viewport={'width':1366,'height':900},color_scheme='light');page=context.new_page();page.set_default_timeout(120000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   url=f'http://127.0.0.1:{server.server_port}/{quote(folder)}/';page.goto(url);page.locator('#themeToggle').wait_for()
   assert page.locator('html').get_attribute('data-theme')=='light'
   values=page.locator('input:not([type=file]),select').evaluate_all('els=>els.map(e=>[e.id,e.value,e.checked])')
   page.locator('#themeToggle').click();assert page.locator('html').get_attribute('data-theme')=='dark'
   assert page.locator('#themeToggle').get_attribute('aria-pressed')=='true'
   assert page.locator('input:not([type=file]),select').evaluate_all('els=>els.map(e=>[e.id,e.value,e.checked])')==values
   assert page.evaluate("getComputedStyle(document.body).backgroundColor==='rgb(16, 28, 38)'")
   page.wait_for_timeout(250)
   page.screenshot(path=str(Path(os.environ['TEMP'])/('theme-'+folder.replace(' ','')+'.png')),full_page=True)
   for width in ([1000] if folder=='EZNesting' else [600,390,320]):
    page.set_viewport_size({'width':width,'height':850});rect=page.locator('#themeToggle').bounding_box();picker=page.locator('#languagePicker').bounding_box()
    assert rect['x']>=0 and rect['x']+rect['width']<=width and picker['x']+picker['width']<=width+1,(folder,width,rect,picker)
   page.set_viewport_size({'width':1366,'height':900})
   page.reload();page.locator('#themeToggle').wait_for();assert page.locator('html').get_attribute('data-theme')=='dark'
   page.locator('#languageButton').click();page.locator('[data-language="en-US"]').click();page.wait_for_function('document.getElementById("themeToggle").title==="Switch to light theme"')
   page.locator('#themeToggle').focus();page.keyboard.press('Enter');assert page.locator('html').get_attribute('data-theme')=='light'
   # Shared origin preference reaches the next project and other open tabs.
   other=context.new_page();other.goto(f'http://127.0.0.1:{server.server_port}/Factory%20Toolbox/');other.locator('#themeToggle').wait_for();other.locator('#themeToggle').click();page.wait_for_function('document.documentElement.dataset.theme==="dark"');other.close()
   page.emulate_media(media='print');assert page.locator('#themeToggle').is_hidden();assert page.evaluate('getComputedStyle(document.documentElement).colorScheme')=='light';page.emulate_media(media='screen')
   assert not errors,(folder,errors)
   print('PASS:',folder,'theme, persistence, cross-page/tab sync, translated labels, keyboard, header and print.',flush=True)
   context.close()
  # A loaded model, its sheet and vector projection survive theme changes.
  context=browser.new_context(color_scheme='dark',viewport={'width':1366,'height':900});page=context.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/View%20and%20Convert/');page.wait_for_function('!!window.ViewConvertCore')
  page.locator('#fileInput').set_input_files({'name':'theme-check.obj','mimeType':'text/plain','buffer':b'v 0 0 0\nv 40 0 0\nv 40 20 0\nv 0 20 0\nv 0 0 30\nv 40 0 30\nv 40 20 30\nv 0 20 30\nf 1 4 3 2\nf 5 6 7 8\nf 1 2 6 5\nf 2 3 7 6\nf 3 4 8 7\nf 4 1 5 8\n'})
  page.locator('#loading').wait_for(state='hidden');dimensions=page.locator('#dimensions').text_content()
  page.screenshot(path=str(Path(os.environ['TEMP'])/'theme-loaded-3D.png'))
  page.locator('#toggleDrawing').click();page.locator('#addDrawingView').click();page.locator('[data-sheet-view]').wait_for()
  geometry=page.locator('[data-sheet-view] path').first.get_attribute('d')
  for _ in range(2):
   page.locator('#themeToggle').click();assert page.locator('#dimensions').text_content()==dimensions;assert page.locator('[data-sheet-view] path').first.get_attribute('d')==geometry
  assert page.locator('#drawingSheet').evaluate('e=>getComputedStyle(e).backgroundColor')=='rgb(255, 255, 255)'
  page.wait_for_timeout(250);page.screenshot(path=str(Path(os.environ['TEMP'])/'theme-loaded-sheet.png'))
  context.close();print('PASS: loaded 3D and sheet preserved, paper stays white.',flush=True)
  context=browser.new_context(color_scheme='dark');page=context.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/Factory%20Toolbox/');page.locator('#themeToggle').wait_for();assert page.locator('html').get_attribute('data-theme')=='dark';page.emulate_media(color_scheme='light');page.wait_for_function('document.documentElement.dataset.theme==="light"');context.close()
  for folder in ['Pipesaver','Best Section','EZNesting']:
   context=browser.new_context();context.add_init_script("localStorage.setItem('factorytoolbox-theme','dark')");page=context.new_page();page.set_default_timeout(120000);page.goto(f'http://127.0.0.1:{server.server_port}/{quote(folder)}/tests/browser-tests.html');page.wait_for_function("['PASS','FAIL'].includes(document.getElementById('status').textContent)")
   assert page.locator('#status').text_content()=='PASS',(folder,page.locator('#details').text_content())
   print('PASS:',folder,'existing application regression in dark theme.',flush=True);context.close()
  browser.close()
finally:server.shutdown()
