from playwright.sync_api import sync_playwright
import time

url = 'file:///C:/Users/FoxOS_User/Developer/f1-race-engineer/index.html'
out = r'C:/Users/FoxOS_User/Developer/f1-race-engineer/'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1560, 'height': 940}, device_scale_factor=1.5)
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(url)
    pg.wait_for_selector('.card', timeout=25000)
    time.sleep(2)
    pg.screenshot(path=out + 'shot-01-grid.png')
    pg.click('.card')  # first driver card
    pg.wait_for_selector('#wall', state='visible', timeout=20000)
    pg.wait_for_selector('#tower .trow', timeout=90000)  # data drained
    time.sleep(2)
    pg.click("button.spd[data-s='120']")
    time.sleep(9)
    pg.screenshot(path=out + 'shot-02-pitwall.png')
    msgs = pg.eval_on_selector_all('#feed .msg', 'els => els.length')
    tower = pg.eval_on_selector_all('#tower .trow', 'els => els.length')
    pos = pg.inner_text('#tPos')
    lap = pg.inner_text('#tLap')
    print('feed msgs:', msgs, '| tower rows:', tower, '| my pos:', pos, '| last lap:', lap)
    print('JS errors:', errs if errs else 'none')
    # mobile pass
    m = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
    m.goto(url)
    m.wait_for_selector('.card', timeout=25000)
    time.sleep(1.5)
    m.screenshot(path=out + 'shot-03-mobile-grid.png')
    m.click('.card')
    m.wait_for_selector('#wall', state='visible', timeout=20000)
    m.wait_for_selector('#tower .trow', timeout=90000)
    time.sleep(2)
    m.screenshot(path=out + 'shot-04-mobile-wall.png')
    b.close()
print('OK')
