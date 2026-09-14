from playwright.async_api import async_playwright

async def inspect_application(url):
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=False);page=await browser.new_page();await page.goto(url,wait_until='domcontentloaded',timeout=60000)
  fields=await page.locator('input,textarea,select,button').evaluate_all("els=>els.map(e=>({tag:e.tagName,type:e.type,name:e.name,placeholder:e.placeholder,text:(e.innerText||'').trim(),required:e.required}))")
  await browser.close();return fields

async def open_application_for_review(url):
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=False);page=await browser.new_page();await page.goto(url,wait_until='domcontentloaded',timeout=60000);await page.pause()
